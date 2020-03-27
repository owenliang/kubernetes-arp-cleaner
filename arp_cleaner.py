from kubernetes import watch, client
from k8s_client import new_client

api_client = new_client()
core_v1 = client.CoreV1Api(api_client)

w = watch.Watch()
for pod in w.stream(core_v1.list_pod_for_all_namespaces):
    print(pod['object'].to_dict())