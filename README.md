# Redirectory

![](https://github.com/kumina/k8s-redirectory/blob/master/documentation/_static/redirectory_logo.png)

Redirectory is a tool that manages redirects on a cluster level.
Requests that would usually end in a **404 PAGE NOT FOUND** can now
redirect to new pages specified with custom rules. It binds itself as
the default backend (essential a wild card) of your ingress controller
and catches all the request that the cluster can't find an ingress rule
for. After that with the help of the
[Hyperscan](https://www.hyperscan.io) regex engine the request is
pernamenty redirected to the new destination from the rules.

# Hyperscan
Before we can use Redirectory you must have the Hyperscan library
installed. Here is a link to the [getting started] documentation. But
we also have prepaired a Docker image. You can find the `Dockerfile` in:
`redirectory/conf/hyperscan-docker` and run the `./build.sh` file. The
interaction between Python and Hyperscan is made with
[python-hyperscan](https://github.com/darvid/python-hyperscan).

# Installation
The best installation experience is with [Helm](https://github.com/helm/helm). 
Just run:
```shell
$ helm install --name=redirectory redirectory/conf/helm
```
More information about this can be found [here](https://redirectory.readthedocs.io/en/latest/misc/install.html).

# Documentation
The documentation is hosted on Read the Docs and can be found at
[redirectory.readthedocs.io](https://redirectory.readthedocs.io).

# License
Redirectory is licensed under the BSD 3-Clause License License. See the
LICENSE file in the project repository.
