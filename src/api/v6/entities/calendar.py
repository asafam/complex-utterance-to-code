from __future__ import annotations
from abc import abstractclassmethod
from entities.generic import Contact, DateTime, Location
from entities.entity import Entity
from entities.resolvable import Resolvable
from typing import Callable, Optional


class CalendarEventType(Entity, Resolvable):
    pass


class CalendarEventName(Entity, Resolvable):
    pass


class CalendarName(Entity, Resolvable):
    pass


class CalendarEvent(Entity):
    date_time: DateTime
    location: Location
    event_name: CalendarEventName
    event_category: CalendarEventType
    calendar: CalendarName

    @abstractclassmethod
    def get_predicate(
        CalendarEvent,
        date_time: Optional[DateTime] = None,
        location: Optional[Contact] = None,
        event_name: Optional[CalendarEventName] = None,
        event_category: Optional[CalendarEventType] = None,
    ) -> Callable[[CalendarEvent], bool]:
        raise NotImplementedError
