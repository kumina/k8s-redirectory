from typing import Union

from flask import make_response, jsonify


def api_error(message: str, errors: Union[str, list], status_code: int):
    """
    Returns an api error with a given status and a message/messages

    Args:
        message: A overall message of the error. E.g. Wrong input.
        errors: A message in str format or a list of strings for multiple error messages
        status_code: The status of the error. E.g. 404, 503 ..
    """
    if isinstance(errors, list):
        return make_response(jsonify({
            "message": message,
            "errors": errors
        }), status_code)
    if isinstance(errors, str):
        return make_response(jsonify({
            "message": message,
            "error": errors
        }), status_code)
    raise AssertionError(f"Messages must be string or list! Not {type(errors).__name__}")
