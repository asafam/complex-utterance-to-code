from __future__ import annotations
from abc import abstractclassmethod, abstractmethod
from typing import TypeVar, Generic, Optional, Union, List
import numpy as np
from entities.entity import Entity
from exceptions.exceptions import exception_handler
from providers.data_model import DataModel
from utils.lang_utils import compute_bleu_score


T = TypeVar("T", bound="Resolvable")


class Resolvable(Generic[T]):
    """
    Markup class
    """

    # @exception_handler
    @classmethod
    def resolve_from_text(T, text: str, recovered_text: Optional[str] = None) -> T:
        data_model = DataModel()
        data = data_model.get_data(T)
        if data is None:
            raise NotImplementedError()

        # items = [x for x in data if x.text == text]

        items = [
            x
            for x in data
            if hasattr(x, "text") and compute_bleu_score(text, x.text) > 0
        ]

        if len(items) == 0:
            raise ValueError()
        else:
            max_index = np.argmax([compute_bleu_score(text, x.text) for x in items])
            result = items[max_index]
            return result

    @classmethod
    def resolve_many_from_text(
        T, text: str, recovered_text: Optional[str] = None
    ) -> List[T]:
        data_model = DataModel()
        data = data_model.get_data(T)
        if data is None:
            raise NotImplementedError()

        # items = [
        #     x for x in data if x.text == text
        # ]  # when resolved many from text we expect the text to be a substring of the actual text

        items = [x for x in data if compute_bleu_score(text, x.text) > 0]

        if len(items) == 0:
            raise ValueError()
        else:
            result = items
            return result

    # @exception_handler
    @classmethod
    def resolve_from_entity(
        T,
        entity: Union[Entity, List[Entity]],
        text: Optional[str] = None,
        recovered_entity: Optional[Union[Entity, List[Entity]]] = None,
    ) -> T:
        data_model = DataModel()
        data = data_model.get_data(T)
        if data is None:
            raise NotImplementedError()

        items = [x for x in data if x.value == entity and (not text or x.text == text)]

        if len(items) == 0:
            raise ValueError()
        else:
            result = items[0]
            return result
