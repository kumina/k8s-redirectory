from redirectory.tests.fixtures import *


class TestDatabaseActions:

    def test_get_or_create(self, database_empty):
        """
        Starts with an empty database.
        Test the get_or_create() function.
        Expected behaviour:
            1. When not existent it should create it and say it is new
            2. If already existent it should return the instance and say it is old
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import db_get_or_create
        from redirectory.models import DomainRule

        # Check with brand new
        domain = 'test.com'
        domain_is_regex = False
        domain_instance, is_new_domain = db_get_or_create(db_session, DomainRule, rule=domain, is_regex=domain_is_regex)
        assert is_new_domain is True
        assert domain_instance.rule == domain
        assert domain_instance.is_regex == domain_is_regex

        # Check existing
        domain_instance, is_new_domain = db_get_or_create(db_session, DomainRule, rule=domain, is_regex=domain_is_regex)
        assert is_new_domain is False
        assert domain_instance.rule == domain
        assert domain_instance.is_regex == domain_is_regex

        # Return session
        DatabaseManager().return_session(db_session)

    def test_encode_model(self, database_populated):
        """
        Starts with an populated database with 5 redirect rules.
        Test the encode_model() function.
        Expected behaviour:
            1. Converts a model to a JSON dict correctly
            2. When the expand settings is used it actually expands the models
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import db_encode_model
        from redirectory.models import RedirectRule

        # Get a model and encode to Json (dict)
        model = db_session.query(RedirectRule).get(1)
        encoded = db_encode_model(model)

        # Check
        assert 'id' in encoded
        assert encoded['id'] == 1
        assert 'weight' in encoded
        assert encoded['weight'] == 100
        assert 'domain_rule' not in encoded

        # Encode with the expand property
        encoded_expanded = db_encode_model(model, expand=True)

        # Check
        assert 'domain_rule' in encoded_expanded
        assert encoded_expanded['domain_rule']['rule'] == 'asd.test.kumina.nl'
        assert 'path_rule' in encoded_expanded
        assert encoded_expanded['path_rule']['rule'] == '/test/path'
        assert 'destination_rule' in encoded_expanded
        assert encoded_expanded['destination_rule']['destination_url'] == 'https://google.com'

        # Return session
        DatabaseManager().return_session(db_session)

    def test_encode_query(self, database_populated):
        """
        Starts with an populated database with 5 redirect rules.
        Test the encode_query() function.
        Expected behaviour:
            1. Converts the query to a JSON dict correctly
            2. When the expand settings is used it actually expands the models
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import db_encode_query
        from redirectory.models import RedirectRule

        # Get a model and encode to Json (dict)
        query = db_session.query(RedirectRule).all()
        encoded = db_encode_query(query)

        # Check
        assert isinstance(encoded, list)
        assert len(encoded) == 5
        assert isinstance(encoded[0], dict)

        # Now with the expand arg
        encoded_expanded = db_encode_query(query, expand=True)

        # Check
        assert isinstance(encoded_expanded, list)
        assert len(encoded_expanded) == 5
        assert isinstance(encoded_expanded[0], dict)
        assert encoded_expanded[0]['id'] == 1

        # Return session
        DatabaseManager().return_session(db_session)

    def test_sanitize_like_query(self, database_empty):
        """
        Starts with an empty db just because we need it to be initialized.
        Test the sanitize_like_query() function.
        Expected behaviour:
            1. Converts the * character to %
            2. Does not convert the * character when escaped
        """
        # Import needed functions and classes
        from redirectory.libs_int.database import db_sanitize_like_query

        # Checks
        result = db_sanitize_like_query('*')
        assert result == '%'

        result = db_sanitize_like_query(r'\*')
        assert result == '*'

        result = db_sanitize_like_query(r'\\*')
        assert result == r'\*'

        result = db_sanitize_like_query(r'\\**\*asd')
        assert result == r'\*%*asd'

        result = db_sanitize_like_query(r'%\**')
        assert result == '%*%'

    def test_get_table_row_count(self, database_populated):
        """
        Starts with an populated database with 5 redirect rules.
        Test the get_table_row_count() function.
        Expected behaviour:
            1. Counts the entries in a table in the DB correctly
            2. When one is deleted the count should decrease
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import db_get_table_row_count
        from redirectory.models import RedirectRule, PathRule

        # Check
        count = db_get_table_row_count(db_session, RedirectRule)
        assert count == 5

        instance: RedirectRule = db_session.query(RedirectRule).get(1)
        instance.delete(db_session)
        count = db_get_table_row_count(db_session, RedirectRule)
        assert count == 4

        count = db_get_table_row_count(db_session, PathRule)
        assert count == 4

        # Return session
        DatabaseManager().return_session(db_session)
