

from abc import abstractmethod
from model import Model
from location import LocationModel
from operators import ComparisonOperator
from arguments import Location, DateTime, Timer, WeatherCondition
from typing import Callable, Optional, Iterator
from entity import TimerEntity


class TimerModel(Model):
    
    def __iter__(self) -> Iterator[TimerEntity]:
        """
        Fetches a model specific iterable
        
        params:
        N/A
        
        retruns:
        An iterable object of Entity instances
        """
        raise NotImplementedError()
    
    @abstractmethod
    def get_predicate(self, 
                      timer_name: Optional[Timer] = None, 
                      op: ComparisonOperator = ComparisonOperator.EQ) -> Callable[[TimerEntity], bool]:
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


