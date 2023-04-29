from __future__ import annotations
from abc import abstractclassmethod
from typing import TypeVar, Type, Generic, Optional, Union, List
from exceptions import exception_handler


T = TypeVar("T", bound="Resolvable")


class Resolvable(Generic[T]):
    """
    Markup class
    """

    @exception_handler
    @abstractclassmethod
    def resolve_from_text(T, text: str, recovered_text: Optional[str] = None) -> T:
        raise NotImplementedError

    @exception_handler
    @abstractclassmethod
    def resolve_from_entity(
        T,
        entity: Union[T, List[T]],
        recovered_entity: Optional[Union[T, List[T]]] = None,
    ) -> T:
        raise NotImplementedError
