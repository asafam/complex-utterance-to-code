from __future__ import annotations
from abc import abstractclassmethod
from entities.entity import Entity
from entities.resolvable import Resolvable
from entities.generic import DateTime, Location
from typing import Callable, Optional


class HomeDeviceName(Entity, Resolvable):
    pass


class HomeDeviceAction(Entity, Resolvable):
    pass


class HomeDeviceValue(Entity, Resolvable):
    pass


class HomeDeviceEntity(Entity):
    pass
