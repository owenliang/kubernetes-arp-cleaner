from kubernetes import watch, client
from k8s_client import new_client
<<<<<<< HEAD
import os

=======
import json
def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
>>>>>>> bebfefdb5d68f2531524e7cfd8dd54c508b9dd90
api_client = new_client()
core_v1 = client.CoreV1Api(api_client)

pods_trace = {}

w = watch.Watch()
for pod in w.stream(core_v1.list_pod_for_all_namespaces):
<<<<<<< HEAD

    op_type = pod['type']
    pod = pod['object'].to_dict()
    fullname = '{}/{}'.format(pod['metadata']['namespace'], pod['metadata']['name'])

    # 我们只对已经trace到的pod做动作，无论是下线还是上线
    if op_type == 'DELETED':
        if fullname in pods_trace:
            traced_pod = pods_trace[fullname]
            if traced_pod['ip']:
                try:
                    cmd = 'arp -d {}'.format(traced_pod['ip'])
                    print('POD offline：', cmd)
                    os.system(cmd)
                except:
                    pass
            del pods_trace[fullname]
    else:
        ip = pod['status']['pod_ip']
        if fullname in pods_trace:
            if pod['status']['pod_ip']:
                try:
                    cmd = 'arp -d {}'.format(pod['status']['pod_ip'])
                    print('POD online：', cmd)
                    os.system(cmd)
                except:
                    pass
            if pods_trace[fullname]['ip'] and not ip:   # 想办法留住POD的IP信息，下线时候好删除用
                ip = pods_trace[fullname]['ip']
        pods_trace[fullname] = {'ip': ip} # 无论如何，trace到这个pod
=======
    print(pod)
    #print(pod['object'].to_dict())
>>>>>>> bebfefdb5d68f2531524e7cfd8dd54c508b9dd90
