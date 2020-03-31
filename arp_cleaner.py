from kubernetes import watch, client
from k8s_client import new_client
import os

# kubernetes客户端
api_client = new_client()
core_v1 = client.CoreV1Api(api_client)

# pod追踪状态
pod_trace_dict = {}

# 清理ARP缓存
def arp_clean(ip):
    try:
        cmd = 'arp -d {}'.format(ip)
        os.system(cmd)
    except:
        return False
    return True

# 开始监听kubernetes的POD变化
w = watch.Watch()
for pod in w.stream(core_v1.list_pod_for_all_namespaces):
    op_type = pod['type']
    pod = pod['object'].to_dict()
    fullname = '{}/{}'.format(pod['metadata']['namespace'], pod['metadata']['name'])

    # 如果pod已追踪
    if fullname in pod_trace_dict:
        traced_pod = pod_trace_dict[fullname]

        # IP补漏
        if not traced_pod['ip']:
            traced_pod['ip'] = pod['status']['pod_ip']

        # 删除则判断是否有ip，有则清理一次arp缓存
        if op_type == 'DELETED':
            if traced_pod['ip']:
                print('[下线清理] POD={}\tIP={}'.format(fullname, traced_pod['ip']))
                arp_clean(traced_pod['ip'])
            del pod_trace_dict[fullname]
        else: # 非删除操作，则进行更新，并判断是否需要clean一次
            if traced_pod['ip'] and not traced_pod['clear_before']: # 有IP地址，并且没有清理过ARP
                print('[上线清理] POD={}\tIP={}'.format(fullname, traced_pod['ip']))
                arp_clean(traced_pod['ip'])
                traced_pod['clear_before'] = True
    else:
        if op_type != 'DELETED':    # 首次被追踪到
            pod_trace_dict[fullname] = {'ip': pod['status']['pod_ip'], 'clear_before': False}
