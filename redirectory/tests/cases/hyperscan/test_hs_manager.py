from redirectory.tests.fixtures import *


class TestHyperscanManager:

    def test_search_domain(self, hyperscan):
        """
        Starts with a populated hyperscan database with 5 rules.
        Test the search_domain() function.
        Expected behaviour:
            1. Returns the correct ids corresponding to the expressions
        """
        # Import needed functions and classes
        from redirectory.libs_int.hyperscan import HsManager, SearchContext

        # Check
        search_ctx: SearchContext = HsManager().search_domain('asd.test.kumina.nl')
        assert search_ctx.matched_ids == [1, 3, 5]

        search_ctx: SearchContext = HsManager().search_domain('123.test.kumina.nl')
        assert search_ctx.matched_ids == [3, 4, 5]

        search_ctx: SearchContext = HsManager().search_domain('123!.test.kumina.nl')
        assert search_ctx.matched_ids == [5]

        search_ctx: SearchContext = HsManager().search_domain('ggg.test.kumina.nl')
        assert search_ctx.matched_ids == [2, 3, 5]

        search_ctx: SearchContext = HsManager().search_domain('test.kumina.nl')
        assert search_ctx.matched_ids == []

    def test_search_rules(self, hyperscan):
        """
        Starts with a populated hyperscan database with 5 rules.
        Test the search_rules() function.
        Expected behaviour:
            1. Returns the correct matched Redirect Rules from the database
        """
        # Import needed functions and classes
        from redirectory.libs_int.hyperscan import HsManager, SearchContext

        # Check
        search_ctx: SearchContext = HsManager().search_rule('1/test/path')
        assert search_ctx.matched_ids == [1]

        search_ctx: SearchContext = HsManager().search_rule('3/test/path/aa')
        assert search_ctx.matched_ids == [3]

        search_ctx: SearchContext = HsManager().search_rule('4/test/path/aa')
        assert search_ctx.matched_ids == [4]

    def test_search(self, hyperscan):
        """
        Starts with a populated hyperscan database with 5 rules.
        Test the search() function.
        Expected behaviour:
            1. Matches the right ids for the right expressions
        """
        # Import needed functions and classes
        from redirectory.libs_int.hyperscan import HsManager

        # Check
        result = HsManager().search(
            domain='asd.test.kumina.nl',
            path='/test/path'
        )
        assert result == [1, 5]

        result = HsManager().search(
            domain='asd.test.kumina.nl',
            path='/test/path/aa'
        )
        assert result == [3, 5]

        result = HsManager().search(
            domain='123.test.kumina.nl',
            path='/test/path'
        )
        assert result == [4, 5]

        result = HsManager().search(
            domain='123!.test.kumina.nl',
            path='/test/path'
        )
        assert result == [5]

        result = HsManager().search(
            domain='123a.test.kumina.nl',
            path='/test/path/a'
        )
        assert result == [3, 5]

        result = HsManager().search(
            domain='ggg.test.kumina.nl',
            path='/test/path/a'
        )
        assert result == [2, 3, 5]

    def test_pick_result(self, hyperscan):
        """
        Starts with a populated hyperscan database with 5 rules.
        Test the pick_result() function.
        Expected behaviour:
            1. Picks the correct one with the highest value
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.hyperscan import HsManager

        # Check
        matched_ids = HsManager().search(
            domain='asd.test.kumina.nl',
            path='/test/path'
        )
        assert matched_ids == [1, 5]
        result, is_ambiguous = HsManager.pick_result(db_session, matched_ids)
        assert is_ambiguous
        assert result.id == 1

        matched_ids = HsManager().search(
            domain='asd.test.kumina.nl',
            path='/test/path/aa'
        )
        assert matched_ids == [3, 5]
        result, is_ambiguous = HsManager.pick_result(db_session, matched_ids)
        assert is_ambiguous
        assert result.id == 3

        matched_ids = HsManager().search(
            domain='123.test.kumina.nl',
            path='/test/path'
        )
        assert matched_ids == [4, 5]
        result, is_ambiguous = HsManager.pick_result(db_session, matched_ids)
        assert is_ambiguous
        assert result.id == 4

        matched_ids = HsManager().search(
            domain='123!.test.kumina.nl',
            path='/test/path'
        )
        assert matched_ids == [5]
        result, is_ambiguous = HsManager.pick_result(db_session, matched_ids)
        assert not is_ambiguous
        assert result.id == 5

        matched_ids = HsManager().search(
            domain='123a.test.kumina.nl',
            path='/test/path/a'
        )
        assert matched_ids == [3, 5]
        result, is_ambiguous = HsManager.pick_result(db_session, matched_ids)
        assert is_ambiguous
        assert result.id == 3

        matched_ids = HsManager().search(
            domain='ggg.test.kumina.nl',
            path='/test/path/a'
        )
        assert matched_ids == [2, 3, 5]
        result, is_ambiguous = HsManager.pick_result(db_session, matched_ids)
        assert is_ambiguous
        assert result.id == 2

        # Return session
        DatabaseManager().return_session(db_session)
