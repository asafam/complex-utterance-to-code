from __future__ import annotations
from abc import abstractclassmethod
from entities.entity import Entity
from entities.resolvable import Resolvable
from entities.generic import DateTime, Location, TimeDuration
from typing import Iterable, Optional


class NavigationDirectionEntity(Entity):
    date_time: DateTime
    source: Location
    destination: Location


class NavigationDistanceEntity(Entity):
    pass


class NavigationDurationEntity(Entity):
    pass


class NavigationEstimatedArrivalEntity(Entity):
    pass


class NavigationEstimatedDepartureEntity(Entity):
    pass


class NavigationTrafficInfoEntity(Entity):
    pass


class NavigationRoadCondition(Entity, Resolvable):
    pass


class NavigationTravelMethod(Entity, Resolvable):
    pass
