==========
 Defaults
==========

You added all you rules but you would like to have a default one.
If there is no other rule that matches the current request then the
default rule will be matched.

Default rules are nothing special. They are just like any other rule you
have been adding so far. It is just a wild card rule.

Global
^^^^^^

Here is an example of a rule that doesn't care about the domain and the path. We
can call this rule a **global** default.

+-----------------+-------------------+-------------------+
|                 | **rule**          | **regex/rewrite** |
+-----------------+-------------------+-------------------+
| **domain**      | .*                | true              |
+-----------------+-------------------+-------------------+
| **path**        | .*                | true              |
+-----------------+-------------------+-------------------+
| **destination** | https://yahoo.com | false             |
+-----------------+-------------------+-------------------+
| **weight**      | 1                 | ---               |
+-----------------+-------------------+-------------------+

.. tip::

   The important thing here is the **weight** of the rule. Default rules must have
   the lowest possible weight. In our case is 1.

Per Domain
^^^^^^^^^^

The nice thing of having it as a normal rule is that we can make defaults
per domain. The only difference is that we need to specify the domain :)

+-----------------+-------------------+-------------------+
|                 | **rule**          | **regex/rewrite** |
+-----------------+-------------------+-------------------+
| **domain**      | kumina.nl         | false             |
+-----------------+-------------------+-------------------+
| **path**        | .*                | true              |
+-----------------+-------------------+-------------------+
| **destination** | https://yahoo.com | false             |
+-----------------+-------------------+-------------------+
| **weight**      | 2                 | ---               |
+-----------------+-------------------+-------------------+

.. tip::

   It is a good practice to have the domain default rules with **weight** one above
   the global default rule you have. In our case the global default rule has a weight of
   **1** therefore this rule should be with **weight** of **2**.

