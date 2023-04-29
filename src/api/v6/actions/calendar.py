from abc import abstractclassmethod
from typing import List, Union, Optional
from entities.resolvable import Resolvable
from entities.generic import *
from entities.calendar import *


class Calendar(Resolvable):
    @abstractclassmethod
    def create_calendar_event(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[CalendarEventName] = None,
        category: Optional[CalendarEventType] = None,
        calendar: Optional[CalendarName] = None,
    ) -> CalendarEvent:
        raise NotImplementedError

    @abstractclassmethod
    def delete_calendar_events(
        cls, events: Optional[Union[CalendarEvent, List[CalendarEvent]]] = None
    ) -> bool:
        raise NotImplementedError

    @abstractclassmethod
    def find_calendar_events(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        event_name: Optional[CalendarEventName] = None,
        event_category: Optional[CalendarEventType] = None,
        calendar: Optional[CalendarName] = None,
    ) -> List[CalendarEvent]:
        raise NotImplementedError
