from abc import abstractmethod
from query import Query
from enum import Enum
from functools import total_ordering


@total_ordering
class Entity():
    
    @abstractmethod
    def get_natural_sorting_value(self) -> any:
        """
        This abstract method should be implmented to return the natural sorting value for this entity.
        The method is called by the Python generic built-in `sort` and `sorted` functions in order to
        compare a collection of Entity objects.
        """
        raise NotImplementedError
    
    def __eq__(self, other: "Entity") -> bool:
        """
        The total_ordering requires the __eq__ and one of the remaining methods to be implemented.
        See more information in the __lt__implementation.
        """
        return self.get_default_sorting_value() == other.get_default_sorting_value()
    
    def __lt__(self, other: "Entity") -> bool:
        """
        According to the Python documentation, the sort and sorted use only the __lt__ 
        magic method when doing sorting. 
        The total_ordering decorator from the functools module helps to reduce the boilerplate. 
        The total_ordering requires the __eq__ and one of the remaining methods to be implemented - the __lt__ method.
        """
        return self.get_default_sorting_value() < other.get_default_sorting_value()
    
    
class EntityDescriptor():
    pass

