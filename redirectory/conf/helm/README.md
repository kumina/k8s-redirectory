# Redirectory

Re->directory is a system for redirecting requests that would usually 
end in a 404 response to a new destination based on specific rules from
the user.

## TL;DR

```bash
# Testing configuration
$ helm install redirectory/conf/helm
```

## Introduction

This chart bootstraps a [Redirectory](https://git.kumina.nl/kubernetes/redirectory) 
deployment on a [Kubernetes](http://kubernetes.io) cluster using the 
[Helm](https://helm.sh) package manager.

## Prerequisites

- Kubernetes 1.8+
- PV provisioner support in the underlying infrastructure

## Installing the Chart

To install the chart with the release name `my-first-release`:

```bash
$ helm install --name my-first-release stable/redirectory
```

The command deploys Redirectory on the Kubernetes cluster in the 
default configuration. The [configuration](#configuration) section lists 
the parameters that can be configured during installation.

> **Tip**: List all releases using `helm list`

## Uninstalling the Chart

To uninstall/delete the `my-first-release` deployment:

```bash
$ helm delete my-first-release
```

The command removes all the Kubernetes components associated with the 
chart and deletes the release.

## Configuration

The following table lists the configurable parameters of the Redirectory
chart and their default values.

| Parameter                                                 | Description                                                                                                    | Default                                              |
|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| `image.tag`                                               | Redirectory Image tag                                                                                          | `latest`                                             |
| `image.pullSecret`                                        | Specify docker-registry secret names as an array                                                               | `none`                                               |
| `image.pullSecretNeeded`                                  | Say if the secret needs to be used or not                                                                      | `false`                                              |
| `image.pullPolicy`                                        | Image pull policy                                                                                              | `Always`                                             |
| `image.management.repository`                             | The registry and path to the image for the Management pod                                                      | `registry.kumina.nl/kumina/redirectory-management`   |
| `image.worker.repository`                                 | The registry and path to the image for the Worker pod                                                          | `registry.kumina.nl/kumina/redirectory-worker`       |
| `management.persistentVolumeClaim.name`                   | The name of the persistent volume for the Management pod                                                       | `redirectory-management`                             |
| `management.persistentVolumeClaim.size`                   | The size of the persistent volume for the Management pod                                                       | `1Gi`                                                |
| `management.persistentVolumeClaim.storageClassName`       | The type of storage class to use for the persistent volume of the Management pod                               | `standard`                                           |
| `management.ingress.host`                                 | On which host should the Management UI be visible                                                              | `redirectory.test.com`                               |
| `management.ingress.path`                                 | Which path for that host should the UI be visible                                                              | `/`                                                  |
| `management.resources`                                    | Resources needed for the management pod                                                                        | `yaml - take a look at values.yaml`                  |
| `worker.replicas`                                         | How many workers should serve redirecting requests                                                             | `3`                                                  |
| `worker.resources`                                        | Resources needed for a single worker pod                                                                       | `yaml - take a look at values.yaml`                  |
| `prometheus.scrape`                                       | If prometheus should scrape directly from the Pod (old)                                                        | `false`                                              |
| `prometheus.operator.enabled`                             | If prometheus should scrape using a service monitor (new)                                                      | `true`                                               |
| `prometheus.operator.namespace`                           | In which namespace is the prometheus operator located. The service minitors should be in the same one          | `infra`                                              |
| `prometheus.operator.serviceMonitor.interval`             | The interval in which the metrics endpoint should be scraped                                                   | `30s`                                                |
| `prometheus.operator.serviceMonitor.selector.prometheus`  | Prometheus serviceMonitorSelector, set to Prometheus release                                                   | `prom`                                               |

The following parameters are the same for both the worker and the
management. The settings are for the liveness and readiness probes for
Kubernetes

| Parameter                                                 | Description                                                                                                    | Default                                              |
|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| `livenessProbe.enabled`                                   | Turn on and off liveness probe                                                                                 | `true`                                               |
| `livenessProbe.initialDelaySeconds`                       | Delay before liveness probe is initiated                                                                       | `30`                                                 |
| `livenessProbe.periodSeconds`                             | How often to perform the probe                                                                                 | `10`                                                 |
| `livenessProbe.timeoutSeconds`                            | When the probe times out                                                                                       | `5`                                                  |
| `livenessProbe.successThreshold`                          | Minimum consecutive successes for the probe to be considered successful after having failed                    | `1`                                                  |
| `livenessProbe.failureThreshold`                          | Minimum consecutive failures for the probe to be considered failed after having succeeded.                     | `6`                                                  |
| `readinessProbe.enabled`                                  | Turn on and off readiness probe                                                                                | `true`                                               |
| `readinessProbe.initialDelaySeconds`                      | Delay before readiness probe is initiated                                                                      | `30`                                                  |
| `readinessProbe.periodSeconds`                            | How often to perform the probe                                                                                 | `10`                                                 |
| `readinessProbe.timeoutSeconds`                           | When the probe times out                                                                                       | `5`                                                  |
| `readinessProbe.successThreshold`                         | Minimum consecutive successes for the probe to be considered successful after having failed                    | `1`                                                  |
| `readinessProbe.failureThreshold`                         | Minimum consecutive failures for the probe to be considered failed after having succeeded.                     | `6`                                                  |

The following settings are under `app:` in both the management and
worker. Those are the settings that are in the config.yaml file that
Redirectory uses in order to configure itself.

| Parameter                         | Description                                                                                                    | Default                                              |
|-----------------------------------|----------------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| `app.deployment`                  | Tells Redirectory in what environment it is running. (`prod`, `dev`, `test`)                                   | `prod`                                               |
| `app.loglevel`                    | The level of logs that will be logged to stdout. (`debug`, `info`, `warning`, `error`, `critical`)             | `info`                                               |
| `app.directories.data`            | The directory where Redirectory expects to find the database                                                   | `/redirectory_data`                                  |
| `app.directories.ui`              | The directory where Redirectory expects to find the UI                                                         | `/redirectory_ui`                                    |
| `app.service.ip`                  | IP the application should listen on                                                                            | `0.0.0.0`                                            |
| `app.service.port`                | Port the application should listen on for normal HTTP requests                                                 | `8001`                                               |
| `app.service.metricsPort`         | Port the Prometheus metrics should be exposed on                                                               | `8002`                                               |
| `app.database.path`               | The path to the DB file including its name. Appended after the `directories.data`                              | `redirectory_sqlite.db`                              |
| `app.hyperscan.domainDb`          | The path to the Hyperscan DB file that stores the Domains. Appended after the `directories.data`               | `hs_compiled_domain.hsd`                             |
| `app.hyperscan.rulesDb`           | The path to the Hyperscan DB file that stores the Redirect Rules. Appended after the `directories.data`        | `hs_compiled_rules.hsd`                              |


Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`. For example,

```bash
$ helm install --name my-release \
  --set image.tag=latest \
    stable/redis
```

The above command sets the Redirectory image tag to `latest`.

Alternatively, a YAML file that specifies the values for the parameters 
can be provided while installing the chart. For example,

```bash
$ helm install --name my-first-release -f values.yaml stable/redirectory
```

> **Tip**: You can use the default [values.yaml](values.yaml)

> **Note for minikube users**: This chart will not work on minikube. 
Please go to the repository and locate the Kubernetes yaml files and 
deploy it manually.
