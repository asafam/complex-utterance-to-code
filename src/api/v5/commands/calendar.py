from abc import abstractclassmethod
from typing import Iterable, Union, Optional
from api.v5.exceptions.resolvable import Resolvable
from typing.generic import Contact, DateTime, Location
from typing.calendar import CalendarEvent, CalendarEventCategory, CalendarEventName, CalendarName


class CalendarCommand(Resolvable):
    
    @abstractclassmethod
    def create_calendar_event(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[CalendarEventName] = None,
        category: Optional[CalendarEventCategory] = None,
        calendar: Optional[CalendarName] = None,
    ) -> CalendarEvent:
        raise NotImplementedError

    @abstractclassmethod
    def delete_calendar_events(
        cls, events: Optional[Union[CalendarEvent, Iterable[CalendarEvent]]] = None
    ) -> bool:
        raise NotImplementedError
