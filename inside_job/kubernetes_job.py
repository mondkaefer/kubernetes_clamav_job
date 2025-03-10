from kubernetes import client
from kubernetes import config
from time import sleep

class Job:

    _job = None
    _job_name = None
    _namespace = None
    _batch_v1_api = None

    def __init__(self, job_name: str, app_label: str, namespace: str, containers: list, pod_restart_policy="Never",
                 backoff_limit=1, parallelism=1):
        self._job_name = job_name
        self._namespace = namespace
        config.load_incluster_config()
        v1_pod_spec = client.V1PodSpec(restart_policy=pod_restart_policy, containers=containers)
        v1_object_meta = client.V1ObjectMeta(labels={"app": app_label})
        v1_pod_template_spec = client.V1PodTemplateSpec(metadata=v1_object_meta, spec=v1_pod_spec)
        v1_job_spec = client.V1JobSpec(template=v1_pod_template_spec, backoff_limit=backoff_limit, parallelism=parallelism)
        v1_object_meta = client.V1ObjectMeta(name=job_name)
        self._job = client.V1Job(api_version="batch/v1", kind="Job", metadata=v1_object_meta, spec=v1_job_spec)
        self._batch_v1_api = client.BatchV1Api()
        pass

    def launch(self, wait_for_completion: bool=True):
        self._batch_v1_api.create_namespaced_job(body=self._job, namespace=self._namespace)
        if wait_for_completion:
            job_completed = False
            while not job_completed:
                status = self.get_status()
                if status.succeeded is not None or status.failed is not None:
                    job_completed = True
                else:
                    sleep(1)

    def get_status(self):
        api_response = self._batch_v1_api.read_namespaced_job_status(name=self._job_name, namespace=self._namespace)
        return api_response.status

    def delete(self, grace_period_seconds=5):
        del_opts = client.V1DeleteOptions(propagation_policy='Foreground', grace_period_seconds=grace_period_seconds)
        self._batch_v1_api.delete_namespaced_job(name=self._job_name, namespace=self._namespace, body=del_opts)