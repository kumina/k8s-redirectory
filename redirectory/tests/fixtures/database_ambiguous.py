import pytest


@pytest.fixture
def database_ambiguous(database_empty):
    from redirectory.libs_int.database import DatabaseManager, add_ambiguous_request

    # Get the database session
    db_session = DatabaseManager().get_session()

    # Add all the rules
    add_ambiguous_request(db_session, 'https://www.google.com')
    add_ambiguous_request(db_session, 'https://www.kumina.nl')
    add_ambiguous_request(db_session, 'https://www.example.com')
    add_ambiguous_request(db_session, 'https://www.test.com')
    add_ambiguous_request(db_session, 'https://www.youtube.com')

    # Return session
    DatabaseManager().return_session(db_session)
