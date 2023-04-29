from __future__ import annotations
from abc import abstractclassmethod
from entities.generic import Contact, Content, DateTime, Location
from entities.entity import Entity
from entities.resolvable import Resolvable
from typing import Callable, Optional


class ReminderEntity(Entity):
    date_time: DateTime
    person_reminded: Contact
    content: Content
