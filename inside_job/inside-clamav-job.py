"""
Creates and deletes a job object.
"""
from time import sleep
from datetime import datetime
from kubernetes import client, config

INGRESS_ID = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
JOB_NAME = f"clamav-scan-{INGRESS_ID}"
NAMESPACE = "default"
CLAMAV_IMAGE = "192.168.64.1:5000/clamav"
SCANNER_IMAGE = "192.168.64.1:5000/sre/clamav_scanner"

def create_job_object():
    # Configure Pod template container
    container1 = client.V1Container(name="clamav", image=CLAMAV_IMAGE, image_pull_policy="Always",
        env=[{"name": "CLAMAV_NO_FRESHCLAMD", "value": "false"}], command=["clamd", "--foreground"])
    container2 = client.V1Container(name="scanner", image=SCANNER_IMAGE,
        command=["python3", "/download_and_scan.py"])
    # Create and configure a spec section
    template = client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(labels={"app": "clamav-scan"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container1, container2]))
    # Create the specification of deployment
    spec = client.V1JobSpec(template=template, backoff_limit=1, parallelism=1)
    # Instantiate the job object
    job = client.V1Job(api_version="batch/v1", kind="Job", metadata=client.V1ObjectMeta(name=JOB_NAME), spec=spec)
    return job

def create_job(api_instance, job):
    api_response = api_instance.create_namespaced_job(body=job, namespace=NAMESPACE)
    get_job_status(api_instance)

def get_job_status(api_instance):
    job_completed = False
    while not job_completed:
        api_response = api_instance.read_namespaced_job_status(name=JOB_NAME, namespace=NAMESPACE)
        if api_response.status.succeeded is not None or api_response.status.failed is not None:
            job_completed = True
        else:
            sleep(1)
            print("Job still active")
    print('Job completed')

def delete_job(api_instance):
    api_response = api_instance.delete_namespaced_job(name=JOB_NAME, namespace=NAMESPACE,
        body=client.V1DeleteOptions(propagation_policy='Foreground', grace_period_seconds=5))
    print("Job deleted")

def main():
    config.load_incluster_config()
    batch_v1 = client.BatchV1Api()
    job = create_job_object()
    create_job(batch_v1, job)
    delete_job(batch_v1)


if __name__ == '__main__':
    main()
