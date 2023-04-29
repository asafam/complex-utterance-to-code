from abc import abstractclassmethod
from typing import Iterable, Optional
from entities.generic import Contact, Content, DateTime
from typing.reminders import Reminder
from exceptions.exceptions import exception_handler


class RemindersQuery:
    @exception_handler
    @abstractclassmethod
    def get_reminders(
        cls,
        person_reminded: Optional[Contact] = None,
        date_time: Optional[DateTime] = None,
        content: Optional[Content] = None,
    ) -> Iterable[Reminder]:
        raise NotImplementedError
