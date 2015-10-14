import inspect
from enum import Enum
import json


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
    elif isinstance(arg[0], tuple) and isinstance(arg, list):
        return json.dumps(dict(arg))
    elif isinstance(arg, dict):
        return json.dumps(arg)
    else:
        return "Invalid type"
