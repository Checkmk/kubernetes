# Monitoring Kubernetes via the Kubernetes agent
For Checkmk 2.1, we are currently building a Kubernetes agent for a more Kubernetes-native monitoring experience. 
Please keep in mind that this is currently experimental and should not be used in production environments.


## Monitoring setup

### What is deployed
The checkmk_agent.yaml file deploys following k8 objects into the cluster:
* checkmk-monitoring namespace
* configmap for a sample certificate
* one service for internal pods communication
* one service for external communication between the cluster and the Checkmk monitoring instance
* one deployment which deploys the cluster-agent pod
* one daemonset which deploys one pod per worker node

---

## How to setup monitoring

The setup consists of two main steps: Deploying to the K8 cluster and setting up the connection from Checkmk

##### Deploy to K8 cluster

`kubectl apply -f checkmk_agent.yaml` will deploy all the objects listed above

Once deployed, the worker-agents will start generating the container metrics and transfer them to the cluster-agents. 
There are no additional setup steps required on the k8 cluster side.


##### Setup connection on Checkmk 

The k8 setup should be up and running before proceeding to the steps listed here. Using `kubectl` retrieve the following
information:


* **Worker Node IP**: using `kubectl get nodes -o wide` retrieve the ip of one of the worker nodes
* **Service Port**: using `kubectl get services -A` retrieve the port of service `checkmk-external` (usually this is 30035)


In the Kubernetes 2.0 Datasource Rule there will be relevant fields under the cluster agent section (this is yet under development)

---
 
##### For POC testing:

For the individual test file, the main function should be called using the appropriate options (worker node ip & 
service port). Calling the file should output the collected pod metrics from all worker nodes. The yaml will create 
the namespace checkmk-monitoring-test instead checkmk-monitoring. After completing the test, feel free to delete 
namespace.
