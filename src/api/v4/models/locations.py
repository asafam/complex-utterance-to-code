from abc import abstractmethod
from model import Model
from operators import ComparisonOperator
from arguments import Location
from typing import Callable, Optional, Iterator
from entity import LocationEntity


class LocationsModel(Model):
    def __iter__(self) -> Iterator[LocationEntity]:
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
        location: Optional[Location] = None,
        op: ComparisonOperator = ComparisonOperator.EQ,
    ) -> Callable[[LocationEntity], bool]:
        """
        An abstract method that upon a semantic role and a query (and an optional entity or operator) should returns a callable (function)
        to judge whether an given input of entity is related to the predicate.

        Example: "Fairlawn, New Jersey"
        location_model = LocationModel("Fairlawn, New Jersey")
        locations = iter(location_model)
        fairlawn_nj = filter(location_model.get_predicate(location=Location.resolve_from_document(doc="Fairlawn, New Jersey")), locations)
        fairlawn_nj = sorted(fairlawn_nj)

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
