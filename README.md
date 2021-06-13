# Deploying Checkmk in Kubernetes 
Ever wanted to set up Checkmk inside Kubernetes?
Here you will find manifests for deploying Checkmk in Kubernetes!

## Getting started basics
1) Download the manifests in Checkmk. 
2) Create the dockerconfigjson for the Checkmk registry and add that to the _checkmk-server_secret-pull-credentials.yaml_
3) kubectl apply -f .

This will create a Checkmk site with the login credentials _cmkadmin // cmk_

Requirements: You need a persistent volume in your cluster.

## Additional configuration options
You will likely have to adjust as well 
- _checkmk-server_ingress.yaml_ (adapt to your ingress set-up)
- _checkmk-server_persistent-volume-claim.yaml_ (adapt to your PV set-up)
- _checkmk-server_secret-site-credentials.yaml_ (for different log-in credentials)

## Help us improve this!
K8s comes in many different shapes and colors. Thus, these manifests might not work completely for you.

Please create a pull request with your recommendation and help us make this better.

## Next steps
We plan to provide helm charts in the future as well. 
