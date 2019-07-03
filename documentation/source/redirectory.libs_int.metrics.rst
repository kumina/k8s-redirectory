redirectory.libs\_int.metrics package
=====================================

Metrics module
^^^^^^^^^^^^^^

Here are a the metrics that are currently being logged by the application:

+------------------------------------------------------+------------------------------------------------------------------+---------------------------------+
| **name**                                             | **Description**                                                  | **label names**                 |
+======================================================+==================================================================+=================================+
| redirectory_requests_duration_seconds                | Time spent processing requests                                   | node_type                       |
+------------------------------------------------------+------------------------------------------------------------------+---------------------------------+
| redirectory_requests_total                           | Number of requests processed                                     | node_type, code                 |
+------------------------------------------------------+------------------------------------------------------------------+---------------------------------+
| redirectory_requests_redirected_duration_seconds     | Time spend processing a redirect request by label                | node_type, measure              |
+------------------------------------------------------+------------------------------------------------------------------+---------------------------------+
| redirectory_requests_redirected_total                | Number of requests that when processed were redirects by label   | node_type, code, request_type   |
+------------------------------------------------------+------------------------------------------------------------------+---------------------------------+
| redirectory_hyperscan_db_compiled_total              | Number of times the management pod has compiled the hyperscan db | node_type                       |
+------------------------------------------------------+------------------------------------------------------------------+---------------------------------+
| redirectory_hyperscan_db_reloaded_total              | Number of times the worker pod has reloaded the hyperscan db     | node_type                       |
+------------------------------------------------------+------------------------------------------------------------------+---------------------------------+
| redirectory_hyperscan_db_version                     | The version of the hyperscan database by node_type               | node_type                       |
+------------------------------------------------------+------------------------------------------------------------------+---------------------------------+

Please fill free to request more that are not in here but you thing might be useful. You can fill in
a `github issue <https://github.com/kumina/k8s-redirectory/issues>`_.

.. automodule:: redirectory.libs_int.metrics.metrics
    :members:
    :undoc-members:
    :show-inheritance:

