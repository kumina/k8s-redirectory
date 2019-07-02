import pytest


def get_domain(session, domain: str, is_regex: bool):
    from redirectory.models import DomainRule
    domain_rule = DomainRule()
    domain_rule.rule = domain
    domain_rule.is_regex = is_regex
    session.add(domain_rule)
    return domain_rule


def get_path(session, path: str, is_regex: bool):
    from redirectory.models import PathRule
    path_rule = PathRule()
    path_rule.rule = path
    path_rule.is_regex = is_regex
    session.add(path_rule)
    return path_rule


def get_destination(session, destination: str, is_rewrite: bool):
    from redirectory.models import DestinationRule
    dest_rule = DestinationRule()
    dest_rule.destination_url = destination
    dest_rule.is_rewrite = is_rewrite
    session.add(dest_rule)
    return dest_rule


def get_redirect_rule(session, domain_rule, path_rule, dest_rule, weight: int = 100):
    from redirectory.models import RedirectRule
    rr = RedirectRule()
    rr.domain_rule = domain_rule
    rr.path_rule = path_rule
    rr.destination_rule = dest_rule
    rr.weight = weight
    session.add(rr)
    return rr


@pytest.fixture
def database_populated(database_empty):
    from redirectory.libs_int.database import DatabaseManager

    session = DatabaseManager().get_session()

    domain_1 = get_domain(session, 'asd.test.kumina.nl', False)
    domain_2 = get_domain(session, 'ggg.test.kumina.nl', False)
    domain_3 = get_domain(session, r'\w+.test.kumina.nl', True)
    domain_4 = get_domain(session, r'\d+.test.kumina.nl', True)
    domain_5 = get_domain(session, r'.*.test.kumina.nl', True)

    path_1 = get_path(session, '/test/path', False)
    path_2 = get_path(session, '/test/path/a.*', True)
    path_3 = get_path(session, '/test/path/.*', True)
    path_4 = get_path(session, '/test/path.*', True)
    path_5 = get_path(session, '/test/pa.*', True)

    dest_1 = get_destination(session, 'https://google.com', False)
    dest_2 = get_destination(session, 'https://youtube.com', False)
    dest_3 = get_destination(session, 'https://kumina.nl', False)
    dest_4 = get_destination(session, 'https://example.com', False)
    dest_5 = get_destination(session, 'https://yahoo.com', False)

    # Get all the ids
    session.flush()

    rr_1 = get_redirect_rule(session, domain_1, path_1, dest_1)
    rr_2 = get_redirect_rule(session, domain_2, path_2, dest_2)
    rr_3 = get_redirect_rule(session, domain_3, path_3, dest_3)
    rr_4 = get_redirect_rule(session, domain_4, path_4, dest_4)
    rr_5 = get_redirect_rule(session, domain_5, path_5, dest_5)

    # Commit everything to DB
    session.commit()

    # Return session
    DatabaseManager().return_session(session)
