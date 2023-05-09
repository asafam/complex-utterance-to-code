from __future__ import annotations
from typing import Any
from abc import abstractclassmethod, abstractmethod


class Entity:
    def __init__(self, **kwargs) -> None:
        super().__init__()
        if kwargs.get("text") is not None:
            kwargs = {**{"value": kwargs.get("text")}, **kwargs}
        self.__dict__.update(kwargs)

    @abstractmethod
    def __gt__(self, other) -> bool:
        raise NotImplementedError()

    def __str__(self) -> str:
        return getattr(self, "text")

    def __eq__(self, other: object) -> bool:
        result = type(self) == type(other)
        result = result and all(getattr(self, attr) == getattr(other, attr) if hasattr(other, attr) else False for attr in self.__dict__.keys())
        result = result and all(getattr(self, attr) == getattr(other, attr) if hasattr(self, attr) else False for attr in other.__dict__.keys())
        return result
