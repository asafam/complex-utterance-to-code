from __future__ import annotations
from abc import abstractclassmethod, abstractmethod
from typing import Iterable
from entity import Entity, EntityProperty, EntityDescriptor
from intent import Intent
from operators import ComparisonOperator
from query import Query


class Model:
    """
    Abstract class that handles data and commands.
    """
    
    @abstractclassmethod
    def get_model(cls, doc: Doc) -> Model:
        """
        A class abstract method that takes a <a href='query.html>Query</a> that shold yield the concretized model instance.
        
        params:
        query (Query): A user query 
        
        returns:
        A model instance
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
    def iter(self) -> Iterable[Entity]:
        """
        Fetches a model specific iterable
        
        params:
        N/A
        
        retruns:
        An iterable object of Entity instances
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
    def get_property(self, doc: Doc) -> EntityProperty:
        """
        An abstract method that should be implemented to return a property within the model that is associated with the given 
        input Query object.
        
        params:
        query (Query): A user query
        
        returns:
        An EntityProperty object
        """
        pass
    
    @abstractmethod
    def get_sort_key(self, keys: EntityProperty|list[EntityProperty]) -> SortKey:
        """
        An abstract method that returns the model's sort keye, which is associate with the given input entity properties.
        When provided with empty keys value this method should return the natural sorting keys for this model. 
        For example, the natural sort key for messages is the date and time field.
        
        params:
        keys (EntityProperty|list[EntityProperty])): A property (or a list of properties) property that should be used as the sort key
        
        returns:
        A sort function of one argument that is used to extract a comparison key from each entity in iterable 
        """
        pass
    
    @abstractmethod
    def get_default_filter(self) -> FilterFunc:
        """
        An abstract method that should return the default filter for the model. For example, for weather model the default filter
        should return the current local weather.
        
        params: 
        N/A
        
        returns:
        A filter function 
        """
        pass
    
    @abstractmethod
    def get_natural_sort_key(self) -> FilterFunc:
        """
        An abstract method that should return the natural sort key for the model. For example, with messages this method
        should return the timestamp of a message as a sort key.
        
        params:
        N/A
        
        returns:
        The natural sort key
        """
        pass
    
    @abstractmethod
    def filter(self, iterable: Iterable[Entity], f: FilterFunc = None) -> Iterable[Entity]:
        """
        This method returns the entities of iterable where filter function f returns True. Upon providing this method with
        an empty filter function values, the natural filter is used (refer to get_default_filter).
        
        params:
        iterable (Iterable[Entity]): An iterable of entities to be filtered
        f (FilterFunc): A filter function of one argument that is used to filter each element in the iterable. 
        
        retuns: 
        Filtered iterable.
        """
        pass
    
    @abstractmethod
    def sort(self, iterable: Iterable[Entity], key: SortKey = None, reverse: bool = False) -> Iterable[Entity]:
        """
        An abstract method that should return the default filter for the model. For example, with weather the default filter
        is the current local weather. When this method is called without a sort key (or None value) it should use the natural 
        sort key
        
        params:
        iterable (Iterable[Entity]): An iterable of entities to be sorted
        key (SortKey): A sort function of one argument that is used to extract a comparison key from each entity in iterable.  
        reverse (bool):  is a boolean value. If set to True, then the list elements are sorted as if each comparison were reversed. 
                         Defauls to False value.
        
        returns:
        A sorted iterable
        """
        pass
    

# FilterFunc = function
# SortKey = function
        