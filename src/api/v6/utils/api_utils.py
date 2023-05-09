from typing import Iterable, TypeVar


T = TypeVar("T")


def first(a: Iterable[T]) -> T:
    first = list(a)[0]
    return first


def last(a: Iterable[T]) -> T:
    first = list(a)[-1]
    return first


def sort(a: Iterable[T], text: str) -> Iterable[T]:
    return sorted(a, key=lambda x: getattr(x, text))


def filter(a: Iterable[T], **kwargs) -> Iterable[T]:
    return [x for x in a if all(hasattr(x, key) and getattr(x, key) == value for key, value in kwargs.items())]
