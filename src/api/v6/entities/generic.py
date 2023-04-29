from __future__ import annotations
from typing import Optional, Union, List
from datetime import datetime
from entities.entity import Entity
from entities.resolvable import Resolvable

# from exceptions.exceptions import NoSuchValueException


class Content(Entity, Resolvable):
    @classmethod
    def resolve_from_entity(
        cls,
        entity: Union[Entity, List[Entity]],
        text: Optional[str] = None,
        recovered_entity: Optional[Union[Entity, List[Entity]]] = None,
    ) -> Content:
        content = Content(value=entity)
        return content


class Contact(Entity, Resolvable):
    pass


class DateTime(Entity, Resolvable):
    value: datetime

    # @classmethod
    # def resolve_from_text(cls, text: str, recovered_text: Optional[str] = None) -> DateTime | List[DateTime]:
    #     data = DataModel.get_data(cls)
    #     if data is None:
    #         raise NotImplementedError()

    #     items = [x for x in data if x.data.get('text') == text]

    #     if len(items) == 0:
    #         raise ValueError()
    #     else:
    #         result = items[0] if len(items) == 1 else items
    #         return result

    # @classmethod
    # def resolve_from_text(
    #     cls,
    #     text: str,
    #     recovered_text: Optional[List[str]] = None
    # ) -> DateTime:
    #     value = None  # replace with actual implementation of inferring the date time from the given input text

    #     if value == None:
    #         payload = {
    #             'text': text
    #         }
    #         raise NoSuchValueException(
    #             payload=payload,
    #             recovery_prompt=f"There is no {text}. Did you mean some other date?",
    #             message=f"There is no {text}",
    #         )

    #     date_time = DateTime()
    #     date_time.value = value
    #     return date_time


class Location(Entity, Resolvable):
    pass


class Amount(Entity, Resolvable):
    pass


class TimeDuration(Entity, Resolvable):
    pass
