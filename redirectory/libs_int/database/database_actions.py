import enum
import decimal
from datetime import date
from typing import Any, Union

from sqlalchemy import func, select
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql.expression import ClauseElement

NoneType = type(None)
"""type: the type of None :D"""


def get_or_create(session, model, defaults=None, **kwargs):
    """
    Gets an instance of an object or if it does not exist then create it.

    Args:
        session: the database session
        model: the model / table to ger or create from
        defaults: any default parameters for creating
        **kwargs: the criteria to get or create

    Returns:
        a tuple(p,q)
        p: an instance of the object and
        q: if it is new or old
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.flush()
        return instance, True


def encode_model(model: DeclarativeMeta, parent_class: Any = None, expand: bool = False) -> dict:
    """
    Encodes a DB instance object of a given model into json

    Args:
        model: The DB model instance to serialize to json
        parent_class: A DB model might inherit from another DB model. Pass the parent class in order to be
                      serialized correctly
        expand: to include relationships or not

    Returns:
        a dictionary with basic data types that are all serializable
    """
    if parent_class is None:
        parent_class = (NoneType,)
    columns = model.__table__.columns.keys() + model.__mapper__.relationships.keys()
    return dict((c, _alchemy_encoder(getattr(model, c), parent_class + (model.__class__,))) for c in columns
                if not c.endswith('_id') and _check_instance(getattr(model, c), parent_class, expand))


def encode_query(query: list, expand: bool = False) -> list:
    """
    Loops through all of the objects in a query and encodes every object
    with the help of encode_model() function. All of the individual encoded
    models are added into a list and then returned.

    Args:
        query: the query that you would like to encode
        expand: if you should expand relationships in the models

    Returns:
        a list of dictionaries which are the encoded objects
    """
    return [encode_model(q, expand=expand) for q in query]


def sanitize_like_query(query_str: str) -> str:
    """
    Sanitizes a string to be used as a query in the DB.
    It will replace a * with % only when the star is not escaped.

    Args:
        query_str: original string to sanitize

    Returns:
        sanitized converted string
    """
    import re
    if query_str.startswith('*'):
        query_str = "%" + query_str[1:]
    query_str = re.sub(r"([^\\])\*", r"\1%", query_str)
    query_str = query_str.replace("\\*", "*")
    return query_str


def get_table_row_count(db_session, model_table) -> int:
    """
    Gets the number of rows in a given database in the given
    database session

    Args:
        db_session: the database session to use for db actions
        model_table: the model / table

    Returns:
        integer represent the number of row in the table
    """
    row_query = select([func.count()]).select_from(model_table)
    row_count = db_session.execute(row_query).scalar()
    return row_count


def _alchemy_encoder(obj: Any, obj_class: Any) -> Union[str, float, int, dict, list]:
    """
    JSON encoder function for SQLAlchemy special classes.

    Args:
        obj: Object to check
        obj_class: The class of the object passed

    Returns:
        Object formatted to acceptable json type
    """
    if isinstance(obj, list):
        return [_alchemy_encoder(i, obj_class) for i in obj] if not isinstance(obj[0], obj_class) else []
    elif isinstance(obj.__class__, DeclarativeMeta):
        return encode_model(obj, obj_class, expand=True)
    elif isinstance(obj, enum.Enum):
        return getattr(obj, 'name')
    elif isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        return obj


def _check_instance(model, parent, expand):
    if isinstance(model.__class__, DeclarativeMeta) and not expand:
        return False
    if isinstance(model, list):
        if len(model) == 0:
            return False
        if isinstance(model[0].__class__, DeclarativeMeta) and not expand:
            return False
        return not isinstance(model[0], parent)
    return not isinstance(model, parent)
