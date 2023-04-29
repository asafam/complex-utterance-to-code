from __future__ import annotations
from abc import abstractclassmethod
from typing.generic import Contact, Content, DateTime, Location, Resolvable, Entity
from typing import Callable, Optional


class Reminder(Entity):
    date_time: DateTime
    person_reminded: Contact
    exact_content: Content

    @abstractclassmethod
    def get_predicate(
        Reminder,
        date_time: Optional[DateTime] = None,
        person_reminded: Optional[Contact] = None,
        exact_content: Optional[Content] = None,
    ) -> Callable[[Reminder], bool]:
        raise NotImplementedError
