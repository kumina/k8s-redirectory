=========
 Testing
=========

For the Redirectory project unit testing is encouraged! The library of
choice to help us with implementing the unit tests is called **PyTest** and
you can see their docs at: `pytest docs <https://docs.pytest.org/en/latest/>`_.


Set up
^^^^^^

Before we start testing Redirectory let's setup our testing environment. There is
already a nice :code:`requirements_test.txt` file we can use for this. You can
create an environment with the following moment:

.. code-block:: bash

   mkvirtualenv redirectory_test -r requirements_test.txt


Running the tests
^^^^^^^^^^^^^^^^^

We can run the tests with the following command:

.. code-block:: bash

   PYTHONPATH=. pytest

and if you would like to see the :code:`stdout` while the tests are running:

.. code-block:: bash

   PYTHONPATH=. pytest -s

Structure
^^^^^^^^^

Because we make use of **pytest** the tests folder is split into two as shown bellow:

.. code-block:: bash

    tests
    ├── cases
    │   ├── database
    │   └── hyperscan
    ├── fixtures
    │   ├── configuration.py
    │   ├── database_ambiguous.py
    │   ├── database_empty.py
    │   ├── database_populated.py
    │   └── hyperscan.py

Fixtures are functions that will run before every test. Let's say
that a certain test needs an already loaded empty database in order to run.
We can create a fixture :code:`database_empty` and add it as a requirement
to this particular unit test.

This is how the :code:`database_empty` fixture would look like:

.. code-block:: Python

   @pytest.fixture
   def database_empty(configuration):
       # Import DB Manager first before the models
       from redirectory.libs_int.database import DatabaseManager

       # Import the models now so that the DB Manager know about them
       import redirectory.models

       # Delete any previous creations of the Database Manager and tables
       DatabaseManager().reload()
       DatabaseManager().delete_db_tables()

       # Create all tables based on the just imported modules
       DatabaseManager().create_db_tables()

.. tip::

   Fixtures can be added as requirements for other fixtures. In this case
   before we can init the database we need to make sure the :code:`configuration` is
   available.

and the unit test will look like this:

.. code-block:: Python

    def test_add_ambiguous_request(self, database_empty):
        """
        Test Description ...
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Here is your actual test
        assert True

        # Return session
        DatabaseManager().return_session(db_session)


.. admonition:: Must do

   Always return the session to the database before your the end of your test
