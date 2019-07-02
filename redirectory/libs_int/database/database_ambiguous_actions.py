from typing import Optional

from kubi_ecs_logger import Logger, Severity

from redirectory.models import AmbiguousRequest
from . import db_get_or_create, get_model_by_id, db_encode_query


def add_ambiguous_request(db_session, new_request_url: str) -> Optional[AmbiguousRequest]:
    """
    Adds a new ambiguous request entry to the database if it doesn't already exists.

    Args:
        db_session: the database session to use for db actions
        new_request_url: the requested url of the ambiguous request

    Returns:
        the instance of the new ambiguous request or None if it already exists
    """
    new_ambiguous, is_new = db_get_or_create(db_session, AmbiguousRequest, request=new_request_url)

    if is_new:
        db_session.commit()
        Logger() \
            .event(category="database", action="ambiguous request added") \
            .log(original=f"Added new ambiguous request with id: {new_ambiguous.id}") \
            .out(severity=Severity.INFO)
        return new_ambiguous
    else:
        Logger() \
            .event(category="database", action="ambiguous request added") \
            .log(original=f"Ambiguous request already exists") \
            .out(severity=Severity.INFO)
        return None


def delete_ambiguous_request(db_session, ambiguous_id: int) -> bool:
    """
    Deletes an ambiguous request with a given id from the database. It is used
    when the ambiguous request is fixed.

    Args:
        db_session: the database session to use for db actions
        ambiguous_id: the id of the ambiguous request to delete

    Returns:
        true if rule deleted successfully else false if rule not found
    """
    result: AmbiguousRequest = get_model_by_id(db_session, AmbiguousRequest, ambiguous_id)
    if result:
        db_session.delete(result)
        db_session.commit()
        Logger() \
            .event(category="database", action="ambiguous request deleted") \
            .log(original=f"Deleted ambiguous request with id: {ambiguous_id}") \
            .out(severity=Severity.INFO)
        return True

    Logger() \
        .event(category="database", action="ambiguous request deleted") \
        .log(original=f"No ambiguous request with id: {ambiguous_id}. Nothing was deleted.") \
        .out(severity=Severity.INFO)
    return False


def list_ambiguous_requests(db_session) -> list:
    """
    List all entries in the Ambiguous request database.
    The function combines the query with the db_encode_query() function
    and returns an already serialized list of JSON object ready to be
    returned by the endpoint.

    Args:
        db_session: the database session to use for queries

    Returns:
        a list of JSON object (python dict) of ambiguous request entries
    """
    query = db_session.query(AmbiguousRequest).all()
    return db_encode_query(query)
