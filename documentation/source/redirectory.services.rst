Services package
============================

This package contains all endpoints that Redirectory has.
Just like other parts of the application the API Endpoints are
also split into different parts:

1. **Management** - All endpoints for management and UI
2. **Worker** - All endpoints for workers
3. **Status** - Endpoints for watching the status of the application
4. **Root** - Endpoints that are bound to **/** (root path). UI for **management** and redirect for **worker**

Contents
^^^^^^^^

.. toctree::

   redirectory.services.worker
   redirectory.services.status
   redirectory.services.management.ambiguous
   redirectory.services.management.database
   redirectory.services.management.kubernetes
   redirectory.services.management.rules
   redirectory.services.management.sync
   redirectory.services.root
