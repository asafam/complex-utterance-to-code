from abc import abstractclassmethod, abstractmethod
from typing import Any, Iterable, Mapping, Union, Optional
from api.v5.exceptions.resolvable import Resolvable
from typing.generic import Contact, DateTime, Entity
from typing.reminders import Content, Reminder
from typing.calendar import CalendarEvent
from exceptions.exceptions import UnderspecificationException


class RemindersCommand(Resolvable):
    @classmethod
    def create_reminder(
        cls,
        date_time: Optional[DateTime] = None,
        person_reminded: Optional[Contact] = None,
        exact_content: Optional[Content] = None,
        calendar_event: Optional[CalendarEvent] = None,
        recovered_args: Optional[Mapping[str, Any]] = None,
    ) -> Reminder:
        if not exact_content:
            payload = {
                "date_time": date_time,
                "person_reminded": person_reminded,
                "exact_content": exact_content,
                "calendar_event": calendar_event,
                "recovered_args": recovered_args,
            }
            raise UnderspecificationException(
                payload=payload,
                recovery_prompt="What should be reminded?",
                message="exact_content argument is missing",
            )
        raise NotImplementedError

    @abstractclassmethod
    def delete_reminders(
        cls, 
        reminders: Union[Reminder, Iterable[Reminder]]
    ) -> bool:
        raise NotImplementedError
