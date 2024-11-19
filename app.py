import os
import yaml
from jinja2 import Environment, FileSystemLoader
import logging

# Configure logging for better traceability
logging.basicConfig(level=logging.INFO)

class EnvReader:
    """Class responsible for reading environment variables from a file."""
    
    def __init__(self, env_file: str):
        self.env_file = env_file
    
    def read(self) -> dict:
        """Read the environment variables from the values file and return as a dictionary."""
        try:
            with open(self.env_file, 'r') as file:
                context = yaml.safe_load(file)
        except FileNotFoundError:
            logging.error(f"Environment file '{self.env_file}' not found.")
            raise
        except Exception as e:
            logging.error(f"Error reading environment variables: {e}")
            raise
        
        # Overwrite with environment variables
        for key, value in os.environ.items():
            if key in context:
                context[key] = value
                
        return context


class TemplateRenderer:
    """Class responsible for rendering Jinja2 templates."""
    
    def __init__(self, template_dir: str):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
    
    def render(self, template_name: str, context: dict) -> str:
        """Render the Jinja2 template with the provided context."""
        try:
            template = self.env.get_template(template_name)
            return template.render(context)
        except Exception as e:
            logging.error(f"Error rendering template '{template_name}': {e}")
            raise


class KubernetesManifestGenerator:
    """Class to manage Kubernetes YAML generation and application."""
    
    def __init__(self, env_file: str, template_dir: str, output_dir: str):
        self.env_reader = EnvReader(env_file)
        self.template_renderer = TemplateRenderer(template_dir)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_yaml_files(self, context: dict) -> None:
        """Generate YAML files from templates."""
        templates = {
            'service.yaml': 'service.yaml.j2',
            'ingress.yaml': 'ingress.yaml.j2',
            'deploy.yaml': 'deploy.yaml.j2',
            'hpa.yaml': 'hpa.yaml.j2'
        }
        
        for file_name, template_name in templates.items():
            try:
                rendered_yaml = self.template_renderer.render(template_name, context)
                output_file_path = os.path.join(self.output_dir, file_name)
                self.write_yaml(output_file_path, rendered_yaml)
                logging.info(f"Generated {output_file_path}")
            except Exception as e:
                logging.error(f"Error generating YAML file for {file_name}: {e}")
                raise

    def write_yaml(self, file_path: str, data: str) -> None:
        """Write rendered YAML data to a file."""
        try:
            with open(file_path, 'w') as file:
                yaml.dump(yaml.safe_load(data), file, default_flow_style=False)
        except Exception as e:
            logging.error(f"Error writing YAML to file '{file_path}': {e}")
            raise
    
    def apply_kubernetes_manifests(self) -> None:
        """Apply the generated Kubernetes YAML files."""
        try:
            os.system(f"kubectl apply -f {self.output_dir}/")
            logging.info(f"Applied Kubernetes resources from {self.output_dir}")
        except Exception as e:
            logging.error(f"Error applying Kubernetes manifests: {e}")
            raise


class App:
    """Main class to orchestrate the workflow."""
    
    def __init__(self, env_file: str, template_dir: str, output_dir: str):
        self.k8s_generator = KubernetesManifestGenerator(env_file, template_dir, output_dir)
    
    def run(self):
        """Run the application by reading env variables, generating YAML, and applying them."""
        try:
            logging.info("Starting application...")
            
            # Read environment variables
            context = self.k8s_generator.env_reader.read()
            
            # Generate the YAML files
            self.k8s_generator.generate_yaml_files(context)
            
            # Apply the Kubernetes resources
            # self.k8s_generator.apply_kubernetes_manifests()
            
            logging.info("Application completed successfully.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise

if __name__ == "__main__":
    # Define paths and filenames
    ENV_FILE = 'values.yaml'  # The values file in the repository
    TEMPLATE_DIR = 'templates'  # Folder containing the Jinja2 templates
    OUTPUT_DIR = 'output'  # Folder where the generated YAML files will be saved
    
    # Create and run the app
    app = App(ENV_FILE, TEMPLATE_DIR, OUTPUT_DIR)
    app.run()