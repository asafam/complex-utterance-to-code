from abc import abstractclassmethod
from __future__ import annotations
from exceptions.resolvable import Resolvable
from typing.generic import Entity, DateTime, Location, TimeDuration
from typing import Callable, Optional


class NavigationDirection(Entity):
    date_time: DateTime
    source: Location
    destination: Location


class NavigationEstimation(Entity):
    duration: TimeDuration
    source: Location
    destination: Location

    @abstractclassmethod
    def get_predicate(
        NavigationEstimation,
        duration: Optional[TimeDuration] = None,
        source: Optional[Location] = None,
        destination: Optional[Location] = None,
    ) -> Callable[[NavigationEstimation], bool]:
        raise NotImplementedError


class NavigationRoute(Entity, Resolvable):
    pass


class TrafficCondition(Entity, Resolvable):
    pass
