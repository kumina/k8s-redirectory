from typing import Union

from kubi_ecs_logger import Logger, Severity
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from redirectory.models import RedirectRule, DomainRule, PathRule, DestinationRule
from . import db_get_or_create

MODEL_PROPERTY_ID_MAP = {
    DomainRule: RedirectRule.domain_rule_id,
    PathRule: RedirectRule.path_rule_id,
    DestinationRule: RedirectRule.destination_rule_id
}


def add_redirect_rule(db_session, domain: str, domain_is_regex: bool, path: str, path_is_regex: bool,
                      destination: str, destination_is_rewrite: bool, weight: int, commit: bool = True) \
        -> Union[RedirectRule, int]:
    """
    Creates a new Redirect Rule from all of the given arguments.
    If a domain, path or destination is already used it is just going to be re-used in the new rule.
    Before all that it validates rules which are rewrites to see if they are configured correctly.

    Depending on where the check failed different integers will be returned.

    Args:
        db_session: the database session to use for the DB actions
        domain: the domain of the new rule
        domain_is_regex: is the domain a regex or not
        path: the path of the new rule
        path_is_regex: is the path a regex or not
        destination: the destination of the new rule
        destination_is_rewrite: is the destination a rewrite or not
        weight: the weight of the new rule
        commit: should the function commit the new rule or just flush for ids

    Returns:
        Redirect Rule - if all went well
        1 (int) - if the check failed for rewrite rule
        2 (int) - if the check for already existing rule failed
    """
    if destination_is_rewrite and not validate_rewrite_rule(path, path_is_regex, destination):
        Logger() \
            .event(category="database", action="rule added") \
            .log(original=f"Rewrite rule failed validation check") \
            .out(severity=Severity.DEBUG)
        return 1

    domain_instance, is_new_domain = db_get_or_create(db_session, DomainRule, rule=domain, is_regex=domain_is_regex)
    path_instance, is_new_path = db_get_or_create(db_session, PathRule, rule=path, is_regex=path_is_regex)
    dest_instance, is_new_dest = db_get_or_create(db_session, DestinationRule, destination_url=destination,
                                                  is_rewrite=destination_is_rewrite)

    new_redirect_rule = RedirectRule()
    new_redirect_rule.domain_rule_id = domain_instance.id
    new_redirect_rule.path_rule_id = path_instance.id
    new_redirect_rule.destination_rule_id = dest_instance.id
    new_redirect_rule.weight = weight
    db_session.add(new_redirect_rule)

    try:
        if commit:
            db_session.commit()
        else:
            db_session.flush()

        Logger() \
            .event(category="database", action="rule added") \
            .log(original=f"Added new redirect rule with id: {new_redirect_rule.id}") \
            .out(severity=Severity.DEBUG)
        return new_redirect_rule
    except IntegrityError:
        Logger() \
            .event(category="database", action="rule added") \
            .log(original=f"Rule already exists") \
            .out(severity=Severity.DEBUG)
        db_session.rollback()
        return 2


def update_redirect_rule(db_session, redirect_rule_id: int, domain: str, domain_is_regex: bool,
                         path: str, path_is_regex: bool, destination: str,
                         destination_is_rewrite: bool, weight: int) \
        -> Union[RedirectRule, int]:
    """
    Updates the rule with the given ID and with the given arguments.
    Finds the rule specified with the redirect_rule_id and updates it's values correspondingly.
    If everything goes correctly then the new version of the rule returned.
    If no rule with that ID is found an integer is returned
    If the new rule fails the rewrite validation an integer is returned

    Args:
        db_session: the database session to use for db actions
        redirect_rule_id: the ID of the rule to update
        domain: the new domain of the rule
        domain_is_regex: the new status of the domain rule
        path: the new path of the rule
        path_is_regex: the new status of the path rule
        destination: the new destination of the rule
        destination_is_rewrite: the new status of the destination rule
        weight: the new weight of the rule

    Returns:
        Redirect Rule - which is the updated version if all went well
        1 (int) - rule exists but fails validation check for rewrite rule
        2 (int) - rule with this id does not exist
    """
    if destination_is_rewrite and not validate_rewrite_rule(path, path_is_regex, destination):
        Logger() \
            .event(category="database", action="rule update") \
            .log(original=f"The new rule updates make the rewrite rule incorrect") \
            .out(severity=Severity.DEBUG)
        return 1

    redirect_rule: RedirectRule = get_model_by_id(db_session, RedirectRule, redirect_rule_id)
    if not redirect_rule:
        Logger() \
            .event(category="database", action="rule update") \
            .log(original=f"A rule with ID: {redirect_rule_id} does not exist") \
            .out(severity=Severity.DEBUG)
        return 2

    domain_instance, _ = db_get_or_create(db_session, DomainRule, rule=domain, is_regex=domain_is_regex)
    path_instance, _ = db_get_or_create(db_session, PathRule, rule=path, is_regex=path_is_regex)
    dest_instance, _ = db_get_or_create(db_session, DestinationRule, destination_url=destination,
                                        is_rewrite=destination_is_rewrite)

    redirect_rule.domain_rule_id = domain_instance.id
    redirect_rule.path_rule_id = path_instance.id
    redirect_rule.destination_rule_id = dest_instance.id
    redirect_rule.weight = weight

    # redirect_rule.save()
    db_session.commit()

    Logger() \
        .event(category="database", action="rule update") \
        .log(original=f"A rule with ID: {redirect_rule_id} has been updated") \
        .out(severity=Severity.DEBUG)
    return redirect_rule


def delete_redirect_rule(db_session, redirect_rule_id: int) -> bool:
    """
    Tries to delete a redirect rule with a given id
    If the rule doesn't exist then false will be returned

    Args:
        db_session: the database session to use for db actions
        redirect_rule_id: the id of the rule to delete

    Returns:
        true if rule deleted successfully else false if rule not found
    """
    result: RedirectRule = get_model_by_id(db_session, RedirectRule, redirect_rule_id)
    if result:
        result.delete(db_session)
        return True
    return False


def get_model_by_id(db_session, model, model_id):
    """
    Queries a specific model / table in a given database session
    for a row with a given ID

    Args:
        db_session: the database session to use for db actions
        model: the model / table to query
        model_id: the id of the given model

    Returns:
        an instance of the model or None if not found
    """
    return db_session.query(model).get(model_id)


def get_usage_count(db_session, model, model_instance_id) -> int:
    """
    Creates a query that counts the usage of a given model with model_instance_id
    in the RedirectRule model / table. After that executes the query and returns the result

    Args:
        db_session: the database session to use for db actions
        model: the model to count the usages for
        model_instance_id: the id of the model instance

    Returns:
        an integer representing how many times a certain model with that id is used
    """
    # Base query
    usage_query = select([func.count()]).select_from(RedirectRule)

    # Append correct where statement to query
    if model in MODEL_PROPERTY_ID_MAP:
        usage_query = usage_query.where(MODEL_PROPERTY_ID_MAP[model] == model_instance_id)

    # Execute query and get number
    usage = db_session.execute(usage_query).scalar()
    return usage


def validate_rewrite_rule(path: str, path_is_regex: bool, destination: str) -> bool:
    """
    Checks if all of the needed variables/placeholders in the destination rule are also appearing
    in the path when compiled to a regex pattern.

    Args:
        path: the path rule to check for
        path_is_regex: if the path rule is a regex (hint in order to pass this check it always has to be)
        destination: the destination rule with placeholders in it

    Returns:
        True if the rule is valid else False
    """
    import re
    import string

    if path_is_regex is False:
        return False

    try:
        # Get the groups from the regex pattern
        path_re_pattern = re.compile(path)
        groups = list(path_re_pattern.groupindex)

        # Get all the variables that need to be replaced
        variables_to_replace = [tup[1] for tup in string.Formatter().parse(destination) if tup[1] is not None]

        if len(groups) != len(variables_to_replace):
            return False

        for var in variables_to_replace:
            if var not in groups:
                return False
        return True
    except Exception:  # All
        return False
