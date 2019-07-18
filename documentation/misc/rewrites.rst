==========
 Rewrites
==========

Redirectory rules have the ability to be a so called rewrite rule.

A rewrite rule is a rule which can extract a given string from the old url
and replace it in the new one and do the redirect. It looks like this:

The user makes a request to:

.. code-block:: bash

   https://asd.test.kumina.nl/id/ac21ca

and the new destination should look like this:

.. code-block:: bash

   https://shop.test.kumina.nl/product/id/ac21ca

In this case we need to transfer the Id (which stays the same) from the old
URL to the new ome. This is done with rewrite rules.

Explanation
^^^^^^^^^^^^

Rewrite rules currently allow you to extract information only from the :code:`path` of
the incoming request. You can place the extracted information anywhere you would like
in the destination :code:`string`.

The extraction from the path is done with Regex capturing groups. If you don't know them
don't worry, they are really simple. Here is an example of a Regex pattern that has a capturing
group in it:

.. code-block:: bash

   /test/path/id/(?P<name_of_group>.*)

Now if we run the following string (in our case URL):

.. code-block:: bash

   /test/path/id/aa_this_is_in_the_group

through the pattern we get the following:

.. code-block:: json

   { "name_of_group": "aa_this_is_in_the_group" }

Now that we know how to extract values from the path with Regex capturing groups
we need to place those values in the destination url and then redirect the user to it.
This is done with so called placeholders in the destination url. They look like this:

.. code-block:: bash

   https://www.some.new.website.com/new/shop/{name_of_group}

After replacing the values in the placeholder we get this:

.. code-block:: bash

   https://www.some.new.website.com/new/shop/aa_this_is_in_the_group

Examples
^^^^^^^^

Here are a couple of examples for you:

+-----------------+--------------------------------------+-------------------+
|                 | **rule**                             | **regex/rewrite** |
+-----------------+--------------------------------------+-------------------+
| **domain**      | test.test.kumina.nl                  | false             |
+-----------------+--------------------------------------+-------------------+
| **path**        | /search/(?P<query>.*)                | true              |
+-----------------+--------------------------------------+-------------------+
| **destination** | https://google.com/search?&q={query} | true              |
+-----------------+--------------------------------------+-------------------+

Now you can search in Google through Kumina :)

You can also have multiple values to extract and replace:

+-----------------+------------------------------------------------+-------------------+
|                 | **rule**                                       | **regex/rewrite** |
+-----------------+------------------------------------------------+-------------------+
| **domain**      | test.test.kumina.nl                            | false             |
+-----------------+------------------------------------------------+-------------------+
| **path**        | /shop/(?P<shop_id>[^/]+)/id/(?P<product_id>.*) | true              |
+-----------------+------------------------------------------------+-------------------+
| **destination** | https://shop.kumina.nl/{shop_id}/{product_id}  | true              |
+-----------------+------------------------------------------------+-------------------+
