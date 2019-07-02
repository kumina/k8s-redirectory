from redirectory.tests.fixtures import *


class TestHyperscanActions:

    def test_get_expressions_and_ids(self, database_populated):
        """
        Starts with a populated database with 5 Redirect Rule entries.
        Test the get_expressions_and_ids() function.
        Expected behaviour:
            1. The function returns the correct output for model Redirect Rule
            1. The function returns the correct output for model Domain RUle
        """
        # Import needed functions and classes
        from redirectory.libs_int.hyperscan import get_expressions_and_ids
        from redirectory.models import RedirectRule, DomainRule

        # Get Redirect Rules
        path_expressions, path_ids = get_expressions_and_ids(db_model=RedirectRule,
                                                             expression_path="path_rule.rule",
                                                             expression_regex_path="path_rule.is_regex",
                                                             id_path="id",
                                                             combine_expr_with="domain_rule.id")

        # Check
        assert path_ids == [1, 2, 3, 4, 5]
        assert path_expressions == [b'1\\/test\\/path', b'2/test/path/a.*', b'3/test/path/.*',
                                    b'4/test/path.*', b'5/test/pa.*']

        # Get Domain Rules
        domain_expressions, domain_ids = get_expressions_and_ids(db_model=DomainRule,
                                                                 expression_path="rule",
                                                                 expression_regex_path="is_regex",
                                                                 id_path="id")

        # Check
        assert domain_ids == [1, 2, 3, 4, 5]
        assert domain_expressions == [b'asd\\.test\\.kumina\\.nl', b'ggg\\.test\\.kumina\\.nl', b'\\w+.test.kumina.nl',
                                      b'\\d+.test.kumina.nl', b'.*.test.kumina.nl']

    def test_multi_getattr(self, mocker):
        """
        Starts with only a mock in order to mock an object to test with.
        Test the multi_getattr() function.
        Expected behaviour:
            1. Returns the correct value in 'sub objects'
        """
        # Import needed functions and classes
        from redirectory.libs_int.hyperscan import multi_getattr

        # Setup test object
        test_object = mocker.MagicMock()

        test_object.values.deployment: str = 'test'
        test_object.values.log_level: str = 'debug'
        test_object.values.node_type: str = 'management'

        test_object.values.directories.data: str = '/home/test/redirectory_data'
        test_object.values.directories.ui: str = '/home/test/redirectory_ui'

        test_object.values.service.ip: str = '0.0.0.0'
        test_object.values.service.port: int = 8001
        test_object.values.service.metrics_port: int = 8002

        # Check
        result = multi_getattr(test_object, 'values.deployment')
        assert result == 'test'
        result = multi_getattr(test_object, 'values.node_type')
        assert result == 'management'
        result = multi_getattr(test_object, 'values.directories.data')
        assert result == '/home/test/redirectory_data'
        result = multi_getattr(test_object, 'values.service.metrics_port')
        assert result == 8002

        result = multi_getattr(test_object, 'values.service.metrics_portaaa')
        assert isinstance(result, mocker.MagicMock)

    def test_get_and_update_hs_db_version(self, database_empty):
        """
        Starts with an empty database.
        Test the get_hs_db_version() function.
        Test the update_hs_db_version() function.
        Expected behaviour:
            1. The get hs db version returns correctly. Including when there is no entry!
            2. Updates new version correctly and moves the old one into the old column in the db.
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.hyperscan import get_hs_db_version, update_hs_db_version, get_timestamp

        # Check
        result = get_hs_db_version()
        assert isinstance(result, tuple)
        assert result[0] is None
        assert result[1] is None

        version_1 = get_timestamp()
        update_hs_db_version(version_1)
        result = get_hs_db_version()
        assert isinstance(result, tuple)
        assert result[0] is None
        assert result[1] == version_1

        version_2 = get_timestamp()
        update_hs_db_version(version_2)
        result = get_hs_db_version()
        assert isinstance(result, tuple)
        assert result[0] == version_1
        assert result[1] == version_2

        # Return session
        DatabaseManager().return_session(db_session)
