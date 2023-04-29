from typing import Iterable, TypeVar
from typing.generic import DateTime

T = TypeVar("T")


def first(a: Iterable[T]) -> T:
    first = list(a)[0]
    return first


def last(a: Iterable[T]) -> T:
    first = list(a)[-1]
    return first


def day_of_the_week(d: DateTime) -> str:
    # ... add implementation here
    return ''
