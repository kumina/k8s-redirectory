import pytest


@pytest.fixture
def hyperscan(database_populated):
    # Import needed things
    from redirectory.libs_int.hyperscan import HsManager, get_expressions_and_ids, get_timestamp
    from redirectory.models import RedirectRule, DomainRule

    domain_expressions, domain_ids = get_expressions_and_ids(db_model=DomainRule,
                                                             expression_path="rule",
                                                             expression_regex_path="is_regex",
                                                             id_path="id")
    HsManager().database.compile_domain_db(domain_expressions, domain_ids)

    path_expressions, path_ids = get_expressions_and_ids(db_model=RedirectRule,
                                                         expression_path="path_rule.rule",
                                                         expression_regex_path="path_rule.is_regex",
                                                         id_path="id",
                                                         combine_expr_with="domain_rule.id")
    HsManager().database.compile_rules_db(path_expressions, path_ids)

    HsManager().database.is_loaded = True
    HsManager().database.db_version = get_timestamp()
