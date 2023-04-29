from __future__ import annotations
from abc import abstractclassmethod, abstractmethod
from typing import Callable, Iterable
from entity import Entity, EntityDescriptor
from intent import Intent
from operators import ComparisonOperator
from query import Query


class Model:
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
        pass
    
    def __iter__(self) -> Iterable[Entity]:
        """
        Fetches a model specific iterable
        
        params:
        N/A
        
        retruns:
        An iterable object of Entity instances
        """
        pass
        
    
    @abstractmethod
    def get_intent(self, doc: Doc) -> Intent:
        """
        A class abstract method that takes and identifier and returns an intent 
        
        params:
        query (Query): A user query
        
        returns:
        An intent class
        """
        pass
    
    @abstractmethod
    def create(self, params: EntityDescriptor) -> Entity:
        """
        Creates a model entity
        
        params:
        params (EntityDescriptor): An entity descriptor that defines the entity
        
        returns:
        A new entity
        """
        pass
    
    @abstractmethod
    def get_predicate(self, doc: Doc, op: ComparisonOperator) -> Callable[[Entity], bool]:
        """
        An abstract method that takes a query and a comparison operator and return a callable (function) that takes as its
        sole input an entity object and return a boolean based on the given comparison operator and the predicate that is applied
        on the entity.
        Fopr example, this method can passed as an argument within Python's built-in filter function. It takes the iterable and apply 
        the predicate together with the comparison operator to judge its participation post applying the filter
        
        params:
        query (Query): A user query
        op (ComparisonOperator): A comparison operator
        
        returns:
        A callable object that takes an entity as its input and return a boolean
        """
        pass
    
    @abstractmethod
    def get_value_extractor(self, doc: Doc) -> Callable[[Entity], any]:
        """
        An abstract method that returns the model's sort keye, which is associate with the given input entity properties.
        When provided with empty keys value this method should return the natural sorting keys for this model. 
        For example, the natural sort key for messages is the date and time field.
        
        params:
        query (Query): A user query
        
        returns:
        A callable object that takes an entity as its input and return a boolean
        """
        pass
        