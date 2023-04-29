from __future__ import annotations
from abc import abstractclassmethod, abstractmethod
from typing import Optional, List
from exceptions.resolvable import Resolvable
from exceptions.exceptions import NoSuchValueException
from datetime import datetime


class Entity:
    @abstractmethod
    def __gt__(self, other) -> bool:
        raise NotImplementedError()
    

class Content(Entity, Resolvable):
    pass 


class Contact(Entity, Resolvable):
    pass


class DateTime(Entity, Resolvable):
    value: datetime

    @classmethod
    def resolve_from_text(
        cls, 
        text: str, 
        recovered_text: Optional[List[str]] = None
    ) -> DateTime:
        value = None  # replace with actual implementation of inferring the date time from the given input text

        if value == None:
            payload = {
                'text': text
            }
            raise NoSuchValueException(
                payload=payload,
                recovery_prompt=f"There is no {text}. Did you mean some other date?",
                message=f"There is no {text}",
            )

        date_time = DateTime()
        date_time.value = value
        return date_time


class Location(Entity, Resolvable):
    pass


class TimeDuration(Entity, Resolvable):
    pass
