from abc import abstractclassmethod
from typing import Iterable, Optional
from entities.generic import DateTime, Location
from typing.calendar import (
    CalendarEventType,
    CalendarEventName,
    CalendarEvent,
    CalendarName,
)


class CalendarQuery:
    @abstractclassmethod
    def get_calendar_events(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[CalendarEventName] = None,
        event_category: Optional[CalendarEventType] = None,
        calendar: Optional[CalendarName] = None,
    ) -> Iterable[CalendarEvent]:
        raise NotImplementedError
