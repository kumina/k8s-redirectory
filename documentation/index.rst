**************************************
Welcome to Redirectory's documentation
**************************************

**Redirectory** is a tool that manages redirects on a cluster level. Requests that would
usually end in a **404 PAGE NOT FOUND** can now redirect to new pages specified with custom rules.
It binds itself as the default backend (essential a wild card) of your ingress controller and
catches all the request that the cluster can't find an ingress rule for.

**KEY FEATURES**
    1. Build to run in Kubernetes.
    2. Easily scalable by spawning new workers.
    3. Can handle multiple domains and sub-domains in a cluster.
    4. Every redirect is represented by a redirect rule. Redirect rules support regex.
    5. Regex matching performed by Intel's open source Hyperscan regex engine.
    6. Can construct new urls by extracting part of old url.
       For example get an id from the old url and place it in the new one.
    7. UI - Easy to use interface so that your marketing people can use it as well.

**AUTHOR**
    **Kumina B.V.** (Ivaylo Korakov)

Install
^^^^^^^
Install Redirectory and creates all the needed resources for it from scratch.

.. code-block:: bash

   helm install --name=redirectory redirectory/conf/helm

For more info on installation take a look at the :ref:`redirectory-installation`.

Documentation
*****************
This part of the documentation will show you how to get started using Redirectory.

.. toctree::
   :maxdepth: 2

   misc/overview
   misc/usage
   misc/install
   misc/kubernetes
   misc/testing
   misc/docs
   misc/license

API Reference
*****************
If you are interested in information about a class, specific function or more
this is the place to take a look.

.. toctree::
   :maxdepth: 3

   source/redirectory

Search documentation
********************
If you are looking for something specific try searching the documentation.

* :ref:`search`
