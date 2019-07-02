from redirectory.tests.fixtures import *


class TestDatabaseAmbiguousActions:

    def test_add_ambiguous_request(self, database_empty):
        """
        Starts with an empty database.
        Test the add_ambiguous_request() function.
        Expected behaviour:
            1. Adds a new entry if non existent already
            2. Returns None if entry already exists
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import add_ambiguous_request, db_get_table_row_count
        from redirectory.models import AmbiguousRequest

        # Check
        new_entry = add_ambiguous_request(db_session, 'https://www.test.com')
        assert new_entry is not None
        assert new_entry.id == 1
        assert new_entry.request == 'https://www.test.com'

        new_entry = add_ambiguous_request(db_session, 'https://www.test.com')
        assert new_entry is None  # Already exists

        new_entry = add_ambiguous_request(db_session, 'https://www.example.com')
        assert new_entry is not None
        assert new_entry.id == 2
        assert new_entry.request == 'https://www.example.com'

        count = db_get_table_row_count(db_session, AmbiguousRequest)
        assert count == 2  # We added 2 ambiguous request

        # Return session
        DatabaseManager().return_session(db_session)

    def test_delete_ambiguous_request(self, database_ambiguous):
        """
        Starts with an populated database with 5 ambiguous request entries
        Test the delete_ambiguous_request() function.
        Expected behaviour:
            1. Deletes an existing entry amd returns True
            2. Tries to delete a non existent entry and returns False
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import delete_ambiguous_request, db_get_table_row_count
        from redirectory.models import AmbiguousRequest

        # Check
        result = delete_ambiguous_request(db_session, 1)
        count = db_get_table_row_count(db_session, AmbiguousRequest)
        assert result
        assert count == 4

        result = delete_ambiguous_request(db_session, 1001)
        assert result is False

        result = delete_ambiguous_request(db_session, 2)
        count = db_get_table_row_count(db_session, AmbiguousRequest)
        assert result
        assert count == 3

        # Return session
        DatabaseManager().return_session(db_session)

    def test_list_ambiguous_requests(self, database_ambiguous):
        """
        Starts with an populated database with 5 ambiguous request entries
        Test the list_ambiguous_requests() function.
        Expected behaviour:
            1. Returns a list of all the entries in the Ambiguous request table
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import list_ambiguous_requests, db_get_table_row_count
        from redirectory.models import AmbiguousRequest

        # Base for comparison
        original_count = db_get_table_row_count(db_session, AmbiguousRequest)

        # Check
        result = list_ambiguous_requests(db_session)
        assert isinstance(result, list)
        assert len(result) == original_count

        # Return session
        DatabaseManager().return_session(db_session)
