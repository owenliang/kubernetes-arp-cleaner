from kubernetes import watch, client
from k8s_client import new_client
import json
def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
api_client = new_client()
core_v1 = client.CoreV1Api(api_client)

w = watch.Watch()
for pod in w.stream(core_v1.list_pod_for_all_namespaces):
    print(pod)
    #print(pod['object'].to_dict())
