# Copyright 2016 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Creates and deletes a job object.
"""

from time import sleep
from kubernetes import client, config

JOB_NAME = "clamav-scan"

def create_job_object():
    # Configure Pod template container
    container1 = client.V1Container(
        name="clamav",
        image="192.168.64.1:5000/clamav",
        command=["clamd", "--foreground"])
    container2 = client.V1Container(
        name="scanner",
        image="192.168.64.1:5000/sre/clamav_scanner",
        command=["python3", "/download_and_scan.py"])
    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "pi"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container1, container2]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=JOB_NAME),
        spec=spec)

    return job


def create_job(api_instance, job):
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace="default")
    print("Job created")
    #print(f"Job created. status='{str(api_response.status)}'")
    get_job_status(api_instance)


def get_job_status(api_instance):
    job_completed = False
    while not job_completed:
        api_response = api_instance.read_namespaced_job_status(name=JOB_NAME, namespace="default")
        if api_response.status.succeeded is not None or api_response.status.failed is not None:
            job_completed = True
        else:
            sleep(1)
            print("Job still active")
    print('Job completed')


def delete_job(api_instance):
    api_response = api_instance.delete_namespaced_job(
        name=JOB_NAME,
        namespace="default",
        body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))
    print("Job deleted")
    #print(f"Job deleted. status='{str(api_response.status)}'")


def main():
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    config.load_kube_config()
    batch_v1 = client.BatchV1Api()
    # Create a job object with client-python API. The job we
    # created is same as the `pi-job.yaml` in the /examples folder.
    job = create_job_object()

    create_job(batch_v1, job)
    delete_job(batch_v1)


if __name__ == '__main__':
    main()
