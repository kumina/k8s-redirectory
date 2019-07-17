import re
from datetime import datetime
from typing import Tuple, List, Optional

import hyperscan as hs
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound

from redirectory.libs_int.database import DatabaseManager
from redirectory.models import HsDbVersion


def get_expressions_ids_flags(db_model: DeclarativeMeta,
                              expression_path: str,
                              expression_regex_path: str,
                              id_path: str,
                              combine_expr_with: str = None) -> Tuple[List[bytes], List[int], List[int]]:
    """
    Gets the expression in the correct format from the database.
    Depending on the arguments the expression can be combined with another piece
    of data. The expression will also be regex escaped if it is a literal.
    If the expression is a regex then a second check will be conducted which checks if the expression
    matches an empty string. If so a different flag than the default is applied.

    Args:
        db_model: The model/table of the current database
        expression_path: The attribute where the expression can be found in the model
        expression_regex_path: The attribute holding the value if an expression is regex or not
        id_path: The attribute where the id can be found
        combine_expr_with: The attribute of extra piece of data that can be appended before the expression

    Returns:
        a tuple containing the expressions, the ids and the flags. tuple(expressions, ids, flags)
    """
    expressions = []
    ids = []
    flags = []

    db_session = DatabaseManager().get_session()

    for instance in db_session.query(db_model):
        expression: str = multi_getattr(instance, expression_path)
        expression_regex: bool = multi_getattr(instance, expression_regex_path)
        expression_id: int = multi_getattr(instance, id_path)

        if combine_expr_with:
            combine_with = multi_getattr(instance, combine_expr_with)
            expression = str(combine_with) + expression

        if expression_regex:
            compiled_ex = re.compile(expression)
            if compiled_ex.search(""):
                flags.append(hs.HS_FLAG_ALLOWEMPTY)
            else:
                flags.append(hs.HS_FLAG_SOM_LEFTMOST)
            del compiled_ex
        else:
            expression = re.escape(expression)
            flags.append(hs.HS_FLAG_SOM_LEFTMOST)

        ids.append(expression_id)
        expressions.append(expression.encode("UTF-8"))

    # Release db session
    DatabaseManager().return_session(db_session)

    return expressions, ids, flags


def multi_getattr(obj, attr, default=None):
    """
    Get a named attribute from an object; multi_getattr(x, 'a.b.c.d') is
    equivalent to x.a.b.c.d. When a default argument is given, it is
    returned when any attribute in the chain doesn't exist; without
    it, an exception is raised when a missing attribute is encountered.
    """
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            if default:
                return default
            else:
                raise
    return obj


def get_timestamp() -> str:
    """
    Gets the current date and time and converts it to epoch

    Returns:
        an epoch string
    """
    return datetime.now().strftime("%s")


def get_hs_db_version() -> Tuple[Optional[str], Optional[str]]:
    """
    Queries the database for the HsDbVersion table which only
    has one entry at all times. Return the two numbers which
    represent the old_version and the current_version of the
    Hyperscan database.

    Returns:
        tuple of old_version and new_version of the Hyperscan Database
    """
    db_session = DatabaseManager().get_session()
    try:
        db_version: HsDbVersion = db_session.query(HsDbVersion).one()
        return db_version.old_version, db_version.current_version
    except NoResultFound:
        return None, None
    finally:
        DatabaseManager().return_session(db_session)


def update_hs_db_version(new_db_version: str = None) -> str:
    """
    Updates the SQLite3 database about the new version of Hyperscan database.

    Returns:
        the new version of the hyperscan database
    """
    # Get new db version if not given
    if new_db_version is None:
        new_db_version: str = get_timestamp()

    from redirectory.models import HsDbVersion
    db_session = DatabaseManager().get_session()

    try:
        db_version: HsDbVersion = db_session.query(HsDbVersion).one()
        db_version.old_version = db_version.current_version
        db_version.current_version = new_db_version
    except NoResultFound:
        new_version = HsDbVersion()
        new_version.current_version = new_db_version
        db_session.add(new_version)

    db_session.commit()
    DatabaseManager().return_session(db_session)
    return new_db_version
