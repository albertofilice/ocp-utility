from kubernetes import client, config
from kubernetes.client.rest import ApiException
import subprocess
import urllib3
import warnings

# Disable warnings for unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Ignore all warnings
warnings.filterwarnings("ignore")

def oc_login(username, password, cluster_url):
    command = f'oc login --username={username} --password={password} --server={cluster_url}'

    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print("Command Output:")
        print(output)
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing the command:")
        print(e.output)

# Example of usage
username = input("Enter the username: ")
password = input("Enter the password: ")
cluster_url = input("Enter the cluster URL: ")

oc_login(username, password, cluster_url)

def check_cluster_health():
    try:
        # Load the configuration from the kubeconfig file
        config.load_kube_config()

        # Create a client object to interact with the Kubernetes/OpenShift API
        v1 = client.CoreV1Api()

        # Get the cluster's status
        component_status = v1.list_component_status()

        # Check the status of the cluster components
        unhealthy_components = []
        for item in component_status.items:
            for condition in item.conditions:
                if condition.status != "True":
                    unhealthy_components.append(item.metadata.name)

        if not unhealthy_components:
            print("The cluster is healthy. All components are in a valid state.")
        else:
            print("The cluster has issues. The following components are unhealthy:")
            for component in unhealthy_components:
                print(component)

        # Get OpenShift Cluster operators
        v1_custom = client.CustomObjectsApi()
        cluster_operators = v1_custom.list_cluster_custom_object(
            group="config.openshift.io",
            version="v1",
            plural="ClusterOperator"
        )

        degraded_operators = []
        for operator in cluster_operators.get("items", []):
            if operator.get("status", {}).get("conditions"):
                for condition in operator["status"]["conditions"]:
                    if condition.get("type") == "Degraded" and condition.get("status") == "True":
                        degraded_operators.append(operator["metadata"]["name"])

        if degraded_operators:
            print("The following Cluster Operators are in a degraded state:")
            for operator in degraded_operators:
                print(operator)
        else:
            print("All Cluster Operators are in a valid state.")

    except ApiException as e:
        print("An error occurred while communicating with the Kubernetes/OpenShift API:")
        print(e)

# Example of usage
check_cluster_health()
