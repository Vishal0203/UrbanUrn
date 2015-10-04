import inspect
from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        props = [m for m in members if not(m[0][:2] == '__')]
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices
