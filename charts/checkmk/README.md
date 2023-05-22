# checkmk

![Version: 1.0.1](https://img.shields.io/badge/Version-1.0.1-informational?style=flat-square) ![AppVersion: 2.1.0p28](https://img.shields.io/badge/AppVersion-2.1.0p28-informational?style=flat-square)

Checkmk Helm chart for Kubernetes. 
This chart deploys a Checkmk server using the official Checkmk Docker image. 
It can deploy a livestatus service for each Checkmk site which can be forwarded by a LoadBalancer to remotely monitor hosts and services on this site. A TLS registration port can also be forwarded to allow agents to register with the Checkmk server.

Checkmk the value table below to see configurable parameters of the chart and their default values. The [values.yaml](./values.yaml) can be used as a reference for how to configure your deployment.

Example values file a deployment with a site and persistent storage. An ingress is deployed so this site can be accessed from outside the cluster:
```yaml

ingress:
  enabled: true
  className: ""
  hosts:
    - host: "" # <- `""`` means any host

sites:
  - name: "site_name"
    passwordSecret: "checkmk-password" # <- Use secret "checkmk-password" to store the password for this site
    persistentVolume:
      enabled: true
      size: 10Gi
      accessMode: ReadWriteOnce
      # storageClass: "local-path"

```

Example values file for two sites on enterprise edition with persistent storage. An ingress is deployed so both sites can be accessed from outside the cluster.
Exposing the Livestatus and TLS registration ports results in iptables forwards being created on the K3S nodes, this emulates a bare metal Checkmk deployment:
```yaml
image:
  repository: registry.checkmk.com/enterprise/check-mk-enterprise

imagePullSecrets:
  - name: regcred

ingress:
  enabled: true
  className: ""
  hosts:
    - host: ""

service:
  http:
    port: 80 # <- Cluster port for the Checkmk server
    type: ClusterIP # <- Since this has an Ingress we don't need a LoadBalancer
    protocol: TCP
    targetPort: 5000 # <- This is the port the Checkmk server listens on in the container
  livestatus:
    port: 6557
    type: LoadBalancer # <- Setting this to LoadBalancer automatically creates iptables forwards in K3S
    protocol: TCP
    targetPort: 6557
  tls:
    port: 8000
    type: LoadBalancer # <- Setting this to LoadBalancer automatically creates iptables forwards in K3S
    protocol: TCP
    targetPort: 8000

sites:
  - name: "site_name"
    passwordSecret: "checkmk-password" # <- Use secret "checkmk-password" to store the password for this site
    persistentVolume:
      enabled: true
      size: 10Gi
      accessMode: ReadWriteOnce
      # storageClass: "local-path"
  - name: "second_site"
    passwordSecret: "checkmk-password" # <- Use secret "checkmk-password" to store the password for this site
    liveStatusPortOverride: 6558 # Overrides the external port for the livestatus service since 6557 is already in use
    tlsPortOverride: 8001 # Overrides the external port for the TLS registration service since 8000 is already in use
    persistentVolume:
      enabled: true
      size: 10Gi
      accessMode: ReadWriteOnce
      # storageClass: "local-path"

```

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Affinity for pod assignment |
| autoscaling.enabled | bool | `false` | Enable autoscaling. Not supported |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| fullnameOverride | string | `""` | Helm chart full name override |
| image.pullPolicy | string | `"IfNotPresent"` | Image pull policy |
| image.repository | string | `"checkmk/check-mk-raw"` | Checkmk image. Use `registry.checkmk.com/enterprise/check-mk-enterprise` for Checkmk Enterprise |
| imagePullSecrets | list | `[]` | Checkmk image pull secrets |
| ingress.annotations | object | `{}` | Ingress annotations |
| ingress.className | string | `""` | Ingress class name |
| ingress.enabled | bool | `false` | Enable ingress |
| ingress.hosts | list | `[{"host":""}]` | Ingress host. Paths will be generated for every site |
| ingress.tls | list | `[]` | Ingress TLS configuration |
| nameOverride | string | `""` | Helm chart release name override |
| nodeSelector | object | `{}` | Node labels for pod assignment |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| replicaCount | int | `1` | Replica count. >1 not supported |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.http.port | int | `80` | Service port to expose the HTTP service on. Override this per site in the `sites` list section |
| service.http.protocol | string | `"TCP"` | Service protocol to expose the HTTP service on |
| service.http.targetPort | int | `5000` | HTTP port in Checkmk containers |
| service.http.type | string | `"ClusterIP"` | Service type to expose the HTTP service on |
| service.livestatus.port | int | `6557` | Service port to expose the livestatus service on. Override this per site in the `sites` list section |
| service.livestatus.protocol | string | `"TCP"` | Service protocol to expose the livestatus service on |
| service.livestatus.targetPort | int | `6557` | Livestatus port in Checkmk containers |
| service.livestatus.type | string | `"ClusterIP"` | Service type to expose the livestatus service on. Set this to LoadBalancer if you want to expose the livestatus port on the host |
| service.tls.port | int | `8000` | Service port to expose the TLS registration service on. Override this per site in the `sites` list section |
| service.tls.protocol | string | `"TCP"` | Service protocol to expose the TLS registration service on |
| service.tls.targetPort | int | `8000` | TLS registration port in Checkmk containers |
| service.tls.type | string | `"ClusterIP"` | Service type to expose the TLS registration service on. Set this to LoadBalancer if you want to expose the TLS registration port on the host |
| serviceAccount.annotations | object | `{}` | Service account annotations |
| serviceAccount.create | bool | `true` | Whether to create a service account |
| serviceAccount.name | string | `""` | Service account name |
| sites[0].httpPortOverride | int | `nil` | Checkmk HTTP port override for this site |
| sites[0].liveStatusPortOverride | int | `nil` | Checkmk livestatus port override for this site. Needs to be set for multiple sites |
| sites[0].name | string | `"checkmk"` | Checkmk site name -- (string) Checkmk site password as plain text |
| sites[0].password | string | `nil` | Checkmk site password as plain text |
| sites[0].passwordSecret | string | `"checkmk-password"` | Secret containing password in "password" field |
| sites[0].persistentVolume.accessMode | string | `"ReadWriteOnce"` | Persistent volume access mode |
| sites[0].persistentVolume.enabled | bool | `false` | Enable persistent storage for this site |
| sites[0].persistentVolume.existingClaim | string | `nil` | Use an existing PVC to persist data |
| sites[0].persistentVolume.size | string | `"10Gi"` | Persistent volume size |
| sites[0].persistentVolume.storageClass | string | `""` | Persistent volume storage class |
| sites[0].tlsPortOverride | int | `nil` | Checkmk TLS port override for this site. Needs to be set for multiple sites |
| sites[0].versionOverride | string | `nil` | Checkmk version override for this site |
| tolerations | list | `[]` | Tolerations for pod assignment |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.0](https://github.com/norwoodj/helm-docs/releases/v1.11.0)
