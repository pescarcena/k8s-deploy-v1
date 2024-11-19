# Kotlin API Deployment Repository

This repository is designed to deploy APIs written in Kotlin. It provides a flexible framework for managing the deployment of Kubernetes resources (such as services, ingress, deployments, and horizontal pod autoscalers) based on configurable environment values.

## Setup and Usage

### Step 1: Create the `values.yaml` file

To configure the deployment, you need to create a `values.yaml` file in the root of the repository. This file should contain the necessary values for the deployment. Here is an example of the `values.yaml` file format:

```yaml
app_name: my-kotlin-api
service_name: my-kotlin-api-service
ingress_name: my-kotlin-api-ingress
ingress_host: mykotlinapi.example.com
service_port: 80
target_port: 8080
container_image: my-kotlin-api:v1
container_port: 8080
replicas: 3
min_replicas: 1
max_replicas: 5
target_cpu_utilization: 80
```

### Step 2: Override values with CLI (Optional)

You can also pass some of the values as command line arguments. These will overwrite the values loaded from values.yaml (or values.txt). For example:

```bash
python app.py --app_name=my-api --service_name=my-service --replicas=5
```

### Step 3: Run the `app.py` script

Once you have the values.yaml file set up, you can use the app.py script to generate Kubernetes YAML files based on the templates and the values provided.

To run the app.py script:

1. Make sure you have Python 3.9 or higher installed.

2. Install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

3. Run the app.py script to generate the Kubernetes YAML files:

```bash
python app.py
```

You can also pass values directly from the CLI, as mentioned earlier, to override the ones in values.yaml.

The script will:

- Read the environment variables from the values.yaml file (and any command line arguments provided).
- Render Kubernetes YAML files for the service, ingress, deployment, and horizontal pod autoscaler.
- Save the generated YAML files in the output/ directory.

### Step 4: Apply the Generated YAML Files

Once the Kubernetes YAML files have been generated, they can be applied to your Kubernetes cluster using the following command:

```bash
kubectl apply -f output/
```

This will deploy the resources to your cluster.

### Folder Structure

The project structure is as follows:

```plaintext
kotlin-api-deployment/
├── app.py               # Python script to generate and apply Kubernetes resources
├── values.yaml          # Configuration file with environment variables for deployment
├── templates/           # Directory containing Jinja2 templates for Kubernetes resources
│   ├── service.yaml.j2
│   ├── ingress.yaml.j2
│   ├── deploy.yaml.j2
│   ├── hpa.yaml.j2
├── output/              # Directory where generated YAML files will be saved
├── requirements.txt     # Python dependencies
└── README.md            # This file
```
