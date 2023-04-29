from abc import abstractclassmethod
from typing import Iterable, Optional
from entities.generic import Content, DateTime, Location
from typing.events import Event, EventType, EventName
from exceptions.exceptions import exception_handler


class RemindersQuery:
    @exception_handler
    @abstractclassmethod
    def get_events(
        cls,
        location: Optional[Location] = None,
        date_time: Optional[DateTime] = None,
        event_name: Optional[EventName] = None,
        event_category: Optional[EventType] = None,
    ) -> Iterable[Event]:
        raise NotImplementedError
