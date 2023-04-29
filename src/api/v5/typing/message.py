from abc import abstractclassmethod
from __future__ import annotations
from exceptions.resolvable import Resolvable
from typing.generic import Contact, Content, DateTime, Location, Entity
from typing import Callable, Optional


class Message(Entity):
    date_time: DateTime
    sender: Contact
    content: Content

    @abstractclassmethod
    def get_predicate(
        Message,
        date_time: Optional[DateTime] = None,
        sender: Optional[Contact] = None,
        content: Optional[Content] = None,
    ) -> Callable[[Message], bool]:
        raise NotImplementedError
