from redirectory.tests.fixtures import *


class TestDatabaseRuleActions:

    def test_add_redirect_rule(self, database_empty):
        """
        Starts with an empty database.
        Test the add_redirect_rule() function.
        Expected behaviour:
            1. Adds a redirect rule correctly
            2. Checks if a rule already exists
            3. Does not create new paths for new rules if they are already used in other rules
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import add_redirect_rule, db_get_table_row_count
        from redirectory.models import RedirectRule, DomainRule, PathRule, DestinationRule

        # Add a two rules
        rule_1: RedirectRule = add_redirect_rule(db_session,
                                                 'kumina.nl', False,
                                                 '/test/path', False,
                                                 'https://new.kumina.nl', False, 100)
        rule_2: RedirectRule = add_redirect_rule(db_session,
                                                 'ivaylo.bg', False,
                                                 '/test', False,
                                                 'https://new.kumina.nl', False, 100)
        rule_3: RedirectRule = add_redirect_rule(db_session,
                                                 'arenabg.com', False,
                                                 '/test', False,
                                                 'https://new.kumina.nl', False, 100)

        # Check
        domain_count = db_get_table_row_count(db_session, DomainRule)
        path_count = db_get_table_row_count(db_session, PathRule)
        destination_count = db_get_table_row_count(db_session, DestinationRule)
        assert domain_count == 3
        assert path_count == 2
        assert destination_count == 1

        assert rule_1.id == 1 and rule_2.id == 2 and rule_3.id == 3
        assert rule_1.path_rule.id == 1
        assert rule_3.path_rule.id == 2

        # Check already existing
        rule_same: RedirectRule = add_redirect_rule(db_session,
                                                    'ivaylo.bg', False,
                                                    '/test', False,
                                                    'https://new.kumina.nl', False, 100)
        assert rule_same is None

        # Return session
        DatabaseManager().return_session(db_session)

    def test_update_redirect_rule(self, database_populated):
        """
        Starts with a populated database with 5 Redirect Rule entries
        Test the update_redirect_rule() function.
        Expected behaviour:
            1. Update the rule correctly
            2. Returns None if rule with that id does not exist
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import update_redirect_rule
        from redirectory.models import RedirectRule

        # Update rule 1
        updated_rule = update_redirect_rule(db_session, 1,
                                            'updated.com', False,
                                            '/new/update', False,
                                            'https://google.com', False, 100)

        # Get the rule from the DB not from the method
        rule: RedirectRule = db_session.query(RedirectRule).get(1)

        # Check
        assert updated_rule is not None
        assert rule.domain_rule.rule == 'updated.com'
        assert rule.path_rule.rule == '/new/update'
        assert rule.destination_rule.destination_url == 'https://google.com'

        # Update non existent rule
        updated_rule = update_redirect_rule(db_session, 1001,
                                            '', False, '', False, '', False, 100)

        # Check
        assert updated_rule is None

        # Return session
        DatabaseManager().return_session(db_session)

    def test_delete_redirect_rule(self, database_populated):
        """
        Starts with a populated database with 5 Redirect Rule entries
        Test the delete_redirect_rule() function.
        Expected behaviour:
            1. Deletes a rule correctly
            2. If a rule does not exist it should return False
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import delete_redirect_rule, db_get_table_row_count
        from redirectory.models import RedirectRule

        # Check deletion
        result = delete_redirect_rule(db_session, 1)
        assert result
        count = db_get_table_row_count(db_session, RedirectRule)
        assert count == 4

        # Check deletion of non existent
        result = delete_redirect_rule(db_session, 1001)
        assert result is False

        # Return session
        DatabaseManager().return_session(db_session)

    def test_get_model_by_id(self, database_populated):
        """
        Starts with a populated database with 5 Redirect Rule entries
        Test the get_model_by_id() function.
        Expected behaviour:
            1. Returns the correct model instance
            2. Returns the correct instance of that model with the given id
            3. Returns None when an instance of that model with id does not exist
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import get_model_by_id
        from redirectory.models import RedirectRule, PathRule

        # Check
        result = get_model_by_id(db_session, RedirectRule, 1)
        assert isinstance(result, RedirectRule)

        result = get_model_by_id(db_session, PathRule, 1)
        assert isinstance(result, PathRule)

        result = get_model_by_id(db_session, PathRule, 100)
        assert result is None

        # Return session
        DatabaseManager().return_session(db_session)

    def test_get_usage_count(self, database_populated):
        """
        Starts with a populated database with 5 Redirect Rule entries
        Test the get_usage_count() function.
        Expected behaviour:
            1. Gets the correct usage of model in the Redirect Rule table
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import get_usage_count, add_redirect_rule
        from redirectory.models import PathRule, DomainRule, DestinationRule

        # Check
        usage = get_usage_count(db_session, DomainRule, 1)
        assert usage == 1

        usage = get_usage_count(db_session, PathRule, 1)
        assert usage == 1

        usage = get_usage_count(db_session, DestinationRule, 1)
        assert usage == 1

        # Add new rules
        add_redirect_rule(db_session,
                          'ggg.test.kumina.nl', False,
                          '/test/path', False,
                          'https://kumina.nl', False, 100)
        add_redirect_rule(db_session,
                          'blabla.test.kumina.nl', False,
                          '/test/path', False,
                          'https://kumina.nl', False, 100)

        # Check again
        usage = get_usage_count(db_session, DomainRule, 2)
        assert usage == 2

        usage = get_usage_count(db_session, PathRule, 1)
        assert usage == 3

        usage = get_usage_count(db_session, DestinationRule, 3)
        assert usage == 3

        # Return session
        DatabaseManager().return_session(db_session)
