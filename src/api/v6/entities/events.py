from __future__ import annotations
from typing import Callable, Optional
from abc import abstractclassmethod
from entities.generic import Contact, Content, DateTime, Location
from entities.entity import Entity
from entities.resolvable import Resolvable


class EventName(Entity, Resolvable):
    pass


class EventCalendar(Entity, Resolvable):
    pass


class EventType(Entity, Resolvable):
    pass


class EventEntity(Entity):
    pass


class EventTicketEntity(Entity):
    pass
