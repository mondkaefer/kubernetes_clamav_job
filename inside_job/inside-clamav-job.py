"""
Creates and deletes a job object.
"""
from datetime import datetime
from kubernetes import client
from kubernetes_job import Job

def main():
    ingress_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    job_name = f"clamav-scan-{ingress_id}"
    namespace = "default"
    clamav_image = "192.168.64.1:5000/clamav"
    scanner_image = "192.168.64.1:5000/sre/clamav_scanner"

    containers = [
        client.V1Container(name="clamav", image=clamav_image, image_pull_policy="Always",
                           env=[{"name": "CLAMAV_NO_FRESHCLAMD", "value": "false"}], command=["clamd", "--foreground"]),
        client.V1Container(name="scanner", image=scanner_image, command=["python3", "/download_and_scan.py"])
    ]
    job = Job(job_name=job_name, app_label="clamd-scan", namespace=namespace, containers=containers)
    job.launch(wait_for_completion=True)
    job.delete()

if __name__ == '__main__':
    main()
