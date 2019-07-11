***************
 Documentation
***************

The documentation is done with Sphinx. This page
will show you how to build the documentation in case
you would like to add something to it.

Preparation
************
We need an environment with the specified packages for the documentation. We can
create a new env like this:

.. code-block:: bash

  $ mkvirtualenv redirectory_docs -r requirements_docs.txt


Now that we have an env we can build the docs but first need to specify
one environment variable that points to the folder which holds
the :code:`config.yaml` file. Here is the command for this:

.. code-block:: bash

  $ export REDIRECTORY_CONFIG_DIR=../redirectory/conf

Build
******
Make sure you have the right environment and the correct env var for the config file.
There is a nice script that will help you with building the docs.

.. code-block:: bash

  $ ./build_docs.sh
