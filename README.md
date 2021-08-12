# Deploying Checkmk in Kubernetes 

Checkmk - Your complete IT monitoring solution. Checkmk is available in several editions. The Checkmk Raw Edition is free and 100% open-source. The following information focuses on deploying Checkmk in a Kubernetes environment. You can check out our [checkmk repository] to find alternative installation methods.



## Getting started basics
1) Download the manifests in the folder checkmk-server/manifests. 
2) Create the dockerconfigjson for the Checkmk registry and add that to the _checkmk-server_secret-pull-credentials.yaml_
3) kubectl apply -f .

This will create a Checkmk site with the login credentials _cmkadmin // cmk_

Requirements: You need a persistent volume in your cluster.

## Additional configuration options
You will likely have to adjust as well 
- _checkmk-server_ingress.yaml_ (adapt to your ingress set-up)
- _checkmk-server_persistent-volume-claim.yaml_ (adapt to your PV set-up)
- _checkmk-server_secret-site-credentials.yaml_ (for different log-in credentials)

## Start monitoring K8s
Follow the instructions on https://docs.checkmk.com/latest/en/monitoring_kubernetes.html

## Help us improve this!
K8s comes in many different shapes and colors. Thus, these manifests might not work completely for you.

Please create a pull request with your recommendation and help us make this better.

## Next steps
We plan to provide helm charts in the future as well. 

## Support
Check out the [Checkmk Forum] where people actively post suggestions for common problems. We also check back regularly, so feel free to make a post describing your problem.

[checkmk repository]: https://github.com/tribe29/checkmk
[Checkmk Forum]: https://forum.checkmk.com/
