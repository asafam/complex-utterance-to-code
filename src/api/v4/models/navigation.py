from abc import abstractmethod
from models.model import Model
from operators import ComparisonOperator
from arguments import Location, DateTime, Route, TrafficCondition
from typing import Callable, Optional, Iterator
from entity import (
    NavigationDirectionsEntity,
    NavigationEstimationEntity,
    TrafficInfoEntity,
)

from document import Doc
from models.locations import LocationsModel


class DirectionsModel(Model):
    def __iter__(self) -> Iterator[NavigationDirectionsEntity]:
        """
        Fetches a model specific iterable

        params:
        N/A

        retruns:
        An iterable object of Entity instances
        """
        raise NotImplementedError()

    @abstractmethod
    def get_predicate(
        self,
        date_time: Optional[DateTime] = None,
        destination: Optional[Location] = None,
        source: Optional[Location] = None,
        op: ComparisonOperator = ComparisonOperator.EQ,
    ) -> Callable[[NavigationDirectionsEntity], bool]:
        """
        An abstract method that upon a semantic role and a query (and an optional entity or operator) 
        should returns a callable (function)
        to judge whether an given input of entity is related to the predicate.

        params:
        source (Location): Optional. The source location of the directions
        destination (Location): Optional. The destination location of the directions
        op (ComparisonOperator): Optional comparison operator. Defaults to op.eq

        returns:
        A callable object that takes an entity as its input and return a boolean
        """
        raise NotImplementedError


class EstimateArrivalModel(Model):
    def __iter__(self) -> Iterator[NavigationEstimationEntity]:
        """
        Fetches a model specific iterable

        params:
        N/A

        retruns:
        An iterable object of Entity instances
        """
        raise NotImplementedError()

    @abstractmethod
    def get_predicate(
        self,
        date_time_arrival: Optional[DateTime] = None,
        source: Optional[Location] = None,
        destination: Optional[Location] = None,
        path: Optional[Route] = None,
        op: ComparisonOperator = ComparisonOperator.EQ,
    ) -> Callable[[NavigationEstimationEntity], bool]:
        """
        An abstract method that upon a semantic role and a query (and an optional entity or operator) should returns a callable (function)
        to judge whether an given input of entity is related to the predicate.

        params:
        param (Param): The query param indicating a semantic role
        query (Query): A user query phrase associated with the semantic role
        entity (Entity|Iterable[Entity]): Optional. Facilitate binding this predicate with a nested lower-level entities set that should provide
            more information on (e.g., a location of an event)
        op (ComparisonOperator): Optional comparison operator. Defaults to op.eq

        returns:
        A callable object that takes an entity as its input and return a boolean
        """
        raise NotImplementedError


class EstimateDepartureModel(Model):
    def __iter__(self) -> Iterator[NavigationEstimationEntity]:
        """
        Fetches a model specific iterable

        params:
        N/A

        retruns:
        An iterable object of Entity instances
        """
        raise NotImplementedError()

    @abstractmethod
    def get_predicate(
        self,
        date_time_arrival: Optional[DateTime] = None,
        source: Optional[Location] = None,
        destination: Optional[Location] = None,
        op: ComparisonOperator = ComparisonOperator.EQ,
    ) -> Callable[[NavigationEstimationEntity], bool]:
        """
        An abstract method that upon a semantic role and a query (and an optional entity or operator) should returns a callable (function)
        to judge whether an given input of entity is related to the predicate.

        params:
        param (Param): The query param indicating a semantic role
        query (Query): A user query phrase associated with the semantic role
        entity (Entity|Iterable[Entity]): Optional. Facilitate binding this predicate with a nested lower-level entities set that should provide
            more information on (e.g., a location of an event)
        op (ComparisonOperator): Optional comparison operator. Defaults to op.eq

        returns:
        A callable object that takes an entity as its input and return a boolean
        """
        raise NotImplementedError


class TrafficInfoModel(Model):
    def __iter__(self) -> Iterator[TrafficInfoEntity]:
        """
        Fetches a model specific iterable

        params:
        N/A

        retruns:
        An iterable object of Entity instances
        """
        raise NotImplementedError()

    @abstractmethod
    def get_predicate(
        self,
        date_time_arrival: Optional[DateTime] = None,
        destination: Optional[Location] = None,
        traffic_condition: Optional[TrafficCondition] = None,
        op: ComparisonOperator = ComparisonOperator.EQ,
    ) -> Callable[[TrafficInfoEntity], bool]:
        """
        An abstract method that upon a semantic role and a query (and an optional entity or operator) should returns a callable (function)
        to judge whether an given input of entity is related to the predicate.

        params:
        param (Param): The query param indicating a semantic role
        query (Query): A user query phrase associated with the semantic role
        entity (Entity|Iterable[Entity]): Optional. Facilitate binding this predicate with a nested lower-level entities set that should provide
            more information on (e.g., a location of an event)
        op (ComparisonOperator): Optional comparison operator. Defaults to op.eq

        returns:
        A callable object that takes an entity as its input and return a boolean
        """
        raise NotImplementedError
