from __future__ import annotations
from abc import abstractmethod
from typing import Callable, Iterable, Iterator
from entity import Entity
from operators import ComparisonOperator
from document import Doc
# from param import Param


class Model():
    """
    Abstract class that handles data and commands.
    """
    
    def __init__(self, doc: Doc):
        """
        The class constructor that takes a <a href='query.html>Query</a> that should yield the concrete model instance.
        
        params:
        query (Query): A user query 
        
        returns:
        A model instance
        """
        raise NotImplementedError()
    
    @abstractmethod
    def get_value_extractor(self, doc: Doc) -> Callable[[Entity], Unknown]:  # type: ignore
        """
        An abstract method that returns the model's sort keye, which is associate with the given input entity properties.
        When provided with empty keys value this method should return the natural sorting keys for this model. 
        For example, the natural sort key for messages is the date and time field.
        
        params:
        query (Query): A user query
        
        returns:
        A callable object that takes an entity as its input and return a boolean
        """
        raise NotImplementedError()
    
        