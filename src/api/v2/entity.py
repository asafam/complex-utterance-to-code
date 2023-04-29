from abc import abstractmethod
from typing import Mapping
from query import Query
from enum import Enum


class Entity():
    
    def __repr__(self):
        """
        This method should be implemented to return the object default value. A possible use case for this method
        is when applying an argument free sort method on an iterable of Entity objects. The sort method will fall back 
        to call this method and it should expect returning the natural sort key.
        """
        pass
    

class SRLProp(Enum):
    """
    Enum of comparison operators
    """
    a0 = 0
    a1 = 1
    a2 = 2
    a_tmp = 3
    a_loc = 4
    a_dir = 5
    
    
class EntityDescriptor(Mapping[SRLProp, Query]):
    pass

