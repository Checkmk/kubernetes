import json
import pprint
import requests

node_ip = "10.200.3.21"  # kubectl get nodes -o wide (node ip address)
service_port = "30036"  # kubectl get services -A (service checkkmk-external port)

resp = requests.get(
    f"https://{node_ip}:{service_port}/cadvisor_container_metrics",
    verify=False
)
if resp.status_code == 200:
    result = {}
    with open("checkmk_k8_raw", "w") as raw_file:
        raw_file.write(resp.content.decode("utf-8"))

    containers = [container for container in json.loads(resp.content)]
    containers_len = len(containers)
    for raw_container in containers:
        name, *metrics = raw_container.split(" ")
        result[name.replace("cName=", "")] = {metric: value for metric, value in (s.split("=") for s in metrics)}

    with open("checkmk_k8.json", "w") as file:
        file.write(json.dumps(result))
else:
    raise RuntimeError(pprint.pformat(resp.json()))

