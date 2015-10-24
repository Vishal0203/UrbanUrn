import inspect
import json
from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        props = [m for m in members if not(m[0][:2] == '__')]
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices


def build_json(arg=None, keys=None, values=None):
    if keys is not None and values is not None:
        return json.dumps(dict(zip(keys, values)))
    elif isinstance(arg, dict):
        return json.dumps(arg)
    elif isinstance(arg, list):
        return json.dumps(arg)
    elif isinstance(arg[0], tuple) and isinstance(arg, list):
        return json.dumps(dict(arg))
    else:
        return "Invalid type"


# Helper method to convert UUID object to string for JSON serialization
def convert_uuid_string(uuid):
    return str(uuid)


# Helper method to convert timestamp object to string for JSON serialization
def format_timestamp(timestamp):
    return str(timestamp)


# Helper method to convert boolean field in request object
def request_boolean_field_value(input_value):
    if input_value.lower() == 'true':
        return True
    else:
        return False
