Models package
==========================

Here as a diagram of the simple database followed by their corresponding classes. I think
they are simple enough to understand directly ;)

.. image:: ../_static/db_diagram.png
   :scale: 100 %
   :alt: Database UML Diagram
   :align: center

The :code:`redirect_rule`, :code:`domain_rule` , :code:`path_rule` and :code:`destination_rule` tables
all have the following two fields:

+--------------+---------------------------------------+----------+-----------+
| **name**     | **Description**                       | **type** | **other** |
+==============+=======================================+==========+===========+
| created_at   | The time this entry was created on    | Datetime | now       |
+--------------+---------------------------------------+----------+-----------+
| modified_at  | The last time the entry was modified  | Datetime | now       |
+--------------+---------------------------------------+----------+-----------+

Redirect Rule
^^^^^^^^^^^^^

+-----------------------+--------------------------------------------------+----------+----------------+
| **name**              | **Description**                                  | **type** | **other**      |
+=======================+==================================================+==========+================+
| id                    | The primary key                                  | Integer  | auto increment |
+-----------------------+--------------------------------------------------+----------+----------------+
| domain_rule_id        | The ID of the domain rule                        | Integer  | foreign key    |
+-----------------------+--------------------------------------------------+----------+----------------+
| path_rule_id          | The ID of the path rule                          | Integer  | foreign key    |
+-----------------------+--------------------------------------------------+----------+----------------+
| destination_rule_id   | The ID of the destination rule                   | Integer  | foreign key    |
+-----------------------+--------------------------------------------------+----------+----------------+
| weight                | The weight/priority of this rule over the others | Integer  | 100            |
+-----------------------+--------------------------------------------------+----------+----------------+

This is how it looks in Python:

.. literalinclude:: ../../redirectory/models/redirect_rule.py
  :language: Python
  :lines: 15, 17, 20, 23, 26


Path Rule
^^^^^^^^^

+-----------+---------------------------------------------------+----------+---------------------+
| **name**  | **Description**                                   | **type** | **other**           |
+===========+===================================================+==========+=====================+
| id        | The primary key                                   | Integer  | auto increment      |
+-----------+---------------------------------------------------+----------+---------------------+
| rule      | The rule that can be regex or literal in a string | String   | required, not null  |
+-----------+---------------------------------------------------+----------+---------------------+
| is_regex  | If the rule is a regex or literal                 | Boolean  | False               |
+-----------+---------------------------------------------------+----------+---------------------+

This is how it looks in Python:

.. literalinclude:: ../../redirectory/models/path_rule.py
  :language: Python
  :lines: 14, 15, 16

Domain Rule
^^^^^^^^^^^

+-----------+---------------------------------------------------+----------+---------------------+
| **name**  | **Description**                                   | **type** | **other**           |
+===========+===================================================+==========+=====================+
| id        | The primary key                                   | Integer  | auto increment      |
+-----------+---------------------------------------------------+----------+---------------------+
| rule      | The rule that can be regex or literal in a string | String   | required, not null  |
+-----------+---------------------------------------------------+----------+---------------------+
| is_regex  | If the rule is a regex or literal                 | Boolean  | False               |
+-----------+---------------------------------------------------+----------+---------------------+

This is how it looks in Python:

.. literalinclude:: ../../redirectory/models/domain_rule.py
  :language: Python
  :lines: 14, 15, 16

Destination Rule
^^^^^^^^^^^^^^^^

+------------------+-----------------------------------------------------+----------+---------------------+
| **name**         | **Description**                                     | **type** | **other**           |
+==================+=====================================================+==========+=====================+
| id               | The primary key                                     | Integer  | auto increment      |
+------------------+-----------------------------------------------------+----------+---------------------+
| destination_url  | The destination URL that can have also placeholders | String   | required, not null  |
+------------------+-----------------------------------------------------+----------+---------------------+
| is_rewrite       | Weather or not the URL has placeholders in it       | Boolean  | False               |
+------------------+-----------------------------------------------------+----------+---------------------+

This is how it looks in Python:

.. literalinclude:: ../../redirectory/models/destination_rule.py
  :language: Python
  :lines: 14, 15, 16

Ambiguous Requests
^^^^^^^^^^^^^^^^^^

+-------------+-------------------------------------------------+----------+---------------------+
| **name**    | **Description**                                 | **type** | **other**           |
+=============+=================================================+==========+=====================+
| id          | The primary key                                 | Integer  | auto increment      |
+-------------+-------------------------------------------------+----------+---------------------+
| request     | The full URL of the request that the worker got | String   | required, not null  |
+-------------+-------------------------------------------------+----------+---------------------+
| created_at  | The time this entry was created on              | Datetime | now                 |
+-------------+-------------------------------------------------+----------+---------------------+

This is how it looks in Python:

.. literalinclude:: ../../redirectory/models/ambiguous_requests.py
  :language: Python
  :lines: 13, 14, 15

Hyperscan DB Version
^^^^^^^^^^^^^^^^^^^^

+------------------+-----------------------------------------------+----------+-------------------+
| **name**         | **Description**                               | **type** | **other**         |
+==================+===============================================+==========+===================+
| id               | The primary key                               | Integer  | auto increment    |
+------------------+-----------------------------------------------+----------+-------------------+
| old_version      | The previous version of the HS database       | String   | nullable          |
+------------------+-----------------------------------------------+----------+-------------------+
| current_version  | The current loaded version of the HS database | String   | required, no null |
+------------------+-----------------------------------------------+----------+-------------------+

This is how it looks in Python:

.. literalinclude:: ../../redirectory/models/hyperscan_db_version.py
  :language: Python
  :lines: 11, 12, 13
