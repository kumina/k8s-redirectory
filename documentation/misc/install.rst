.. _redirectory-installation:

**************
 Installation
**************

The application is made to run on a **Kubernetes** cluster.
There are a few things you need to have in order to deploy it.

1. **Persistent Volume** - In order for the management pod to store the rules (data) in case
   of a failure or restart. Workers don't have persistent volumes. They sync their data from the
   management pod.
2. **Role bindings** - Needed because the application must know of worker and management pods.
   The following permissions are needed for a Role resource:

+---------------+------------------+
| **resources** | **verbs**        |
+---------------+------------------+
| endpoints     | get, list, watch |
+---------------+------------------+
| pods          | get, list, watch |
+---------------+------------------+

You would be able to find all the **.yaml** configuration files in the Redirectory repository.

Installation manually
*********************
This installation method is NOT recommended!
All of the needed configuration files are located under the folder:

.. code-block:: bash

  $ redirectory/conf/kubernetes

You will have to apply all the files manually to your cluster with the following command:

.. code-block:: bash

   $ kubectl apply -f management_ingress.yaml
   $ kubectl apply -f management_svc.yaml -f worker_svc.yaml
   ... and so on

You may or may not need to edit the configuration files to fit your particular setup.

Installation with HELM
**********************
To make the installation easier we are making use of HELM. It is a soft of package
manager for Kubernetes but more like a templating engine for Kubernetes **.yaml** configuration files.

If you are not familiar with HELM please take a look at theirs documentation on how to use it:
`HELM docs <https://helm.sh/docs/>`_

Before continuing make sure you have HELM installed on your kubernetes cluster.

Install
^^^^^^^
Install Redirectory and creates all the needed resources for it from scratch.

.. code-block:: bash

   $ helm install --name=redirectory redirectory/conf/helm

Update
^^^^^^^
Updates only the resources/things that have changes since the last update or install
of Redirectory

.. code-block:: bash

   $ helm upgrade redirectory redirectory/conf/helm

Delete
^^^^^^^
Deletes Redirectory from the Kubernetes cluster.

.. warning::

    When deleting the application like this it will also DELETE ALL it's data.
    You will not be able to get the data back.

.. code-block:: bash

   $ helm delete --purge redirectory
