Redirectory API Reference
=========================

This part of the documentation is for developers who would like
to know the insides of the project. Here you will find all of the
documentation of the source code of Redirectory.

| The project is split into different packages for better structure.
| Here is a quick overview of all of the packages that the project consists of:

**libs_int** overview
^^^^^^^^^^^^^^^^^^^^^
Libs_int is the main package that holds most of the main logic of the application.
The main goal is to move out the logic from the API endpoints themselves and have it
in one place.
This package holds logic for quite a few things:

1. **Config** - .yaml configuration files
2. **Database** - all the needed classes and methods to interact with the database
3. **Hyperscan** - all of the logic of the Hyperscan regex engine
4. **Importers** - different file importers. At the moment only CSV.
5. **Metrics** - logic about Prometheus metrics
6. **Service** - helper classes and methods for API functionality. Also Gunicorn.

**models** overview
^^^^^^^^^^^^^^^^^^^
Redirectory uses a **SQLite3** database which sits as a file in the **data folder** of
the application. The Models packages contains the different models for the database.
Redirectory is using **SQLAlchemy** library to the it's interactions with the database.

**runnables** overview
^^^^^^^^^^^^^^^^^^^^^^
Again because Redirectory is made for Kubernetes we split up the application in three different parts:

1. Management
2. Worker
3. Compiler

Because of this we need a nice way to separate between those different modes.
Here the **runnables** come in play. A runnable is a class which makes use of the
:code:`run()` method which loads different things and prepares the application to
run in the correct mode.

**services** overview
^^^^^^^^^^^^^^^^^^^^^^
The service package is where all of the different API endpoints are situated.
Because the application is made for Kubernetes there are a few different modes
that Redirectory can run as. Therefore the API endpoints are split in the same manner:

1. Management Endpoints
2. Worker Endpoints

Based on the **node_type** which is specified in the **config.yaml** the different sets
of API endpoints are loaded at startup. In other words, if you run the application
as **management** you won't be able to call **worker** endpoints and the other way around.

.. important::

    Keep in mind the **stats** endpoints are loaded in both **management and worker** mode.


Contents
^^^^^^^^

.. toctree::

    redirectory.libs_int
    redirectory.models
    redirectory.runnables
    redirectory.services

