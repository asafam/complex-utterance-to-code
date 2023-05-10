from __future__ import annotations
from abc import abstractclassmethod
from entities.entity import Entity
from entities.resolvable import Resolvable
from entities.generic import Contact, Content, DateTime, Location
from typing import Callable, Optional


class MessageEntity(Entity):
    pass


class MessageStatus(Entity, Resolvable):
    pass


class MessageContentType(Entity, Resolvable):
    pass
