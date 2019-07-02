from redirectory.tests.fixtures import *


class TestDatabasePagination:

    def test_paginate(self, database_populated):
        """
        Starts with a populated database with 5 Redirect Rule entries.
        Test the paginate() function.
        Expected behaviour:
            1. Gathers the correct amount of entries into a Page
            2. Calculates correctly if there are other pages
            3. Calculates the total correctly
        """
        # Get session
        from redirectory.libs_int.database import DatabaseManager
        db_session = DatabaseManager().get_session()

        # Import needed functions and classes
        from redirectory.libs_int.database import paginate, Page
        from redirectory.models import RedirectRule

        # Check
        query = db_session.query(RedirectRule)
        page: Page = paginate(query, 1, 3)
        assert isinstance(page, Page)
        assert len(page.items) == 3
        assert page.next_page == 2
        assert page.has_next
        assert not page.has_previous
        assert page.pages == 2
        assert page.total == 5

        # Check
        query = db_session.query(RedirectRule)
        page: Page = paginate(query, 1, 5)
        assert isinstance(page, Page)
        assert len(page.items) == 5
        assert page.next_page is None
        assert not page.has_next
        assert not page.has_previous
        assert page.pages == 1
        assert page.total == 5

        # Return session
        DatabaseManager().return_session(db_session)
