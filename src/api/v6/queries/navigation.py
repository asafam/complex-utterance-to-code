from abc import abstractclassmethod
from typing import Iterable, Optional
from entities.generic import Contact, Content, DateTime, Location
from typing.navigation import (
    NavigationDirection,
    NavigationEstimation,
    NavigationRoute,
    TrafficCondition,
)
from exceptions.exceptions import exception_handler


class NavigationQuery():
    
    @abstractclassmethod
    def find_directions(
        cls,
        date_time: Optional[DateTime] = None,
        destination: Optional[Location] = None,
        source: Optional[Location] = None,
    ) -> Iterable[NavigationDirection]:
        raise NotImplementedError

    @abstractclassmethod
    def find_estimated_arrival(
        cls,
        departure_date_time: Optional[DateTime] = None,
        destination: Optional[Location] = None,
        source: Optional[Location] = None,
        route: Optional[NavigationRoute] = None,
    ) -> Iterable[NavigationEstimation]:
        raise NotImplementedError

    @abstractclassmethod
    def find_estimated_departure(
        cls,
        arrival_date_time: Optional[DateTime] = None,
        destination: Optional[Location] = None,
        source: Optional[Location] = None,
        route: Optional[NavigationRoute] = None,
    ) -> Iterable[NavigationEstimation]:
        raise NotImplementedError

    @abstractclassmethod
    def find_traffic_info(
        cls,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
        traffic_condition: Optional[TrafficCondition] = None,
        route: Optional[NavigationRoute] = None,
    ) -> Iterable[NavigationEstimation]:
        raise NotImplementedError
