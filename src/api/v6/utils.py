from typing import Iterable, TypeVar
from entities.generic import DateTime

T = TypeVar("T")


def first(a: Iterable[T]) -> T:
    first = list(a)[0]
    return first


def last(a: Iterable[T]) -> T:
    first = list(a)[-1]
    return first


def sort(a: Iterable[T], text: str) -> Iterable[T]:
    return sorted(a, key=lambda x: x.data.get(text))
