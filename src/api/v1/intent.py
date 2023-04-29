from __future__ import annotations
from abc import abstractmethod
from entity import Entity


class Intent:
    """
    Intent class
    """
    
    @abstractmethod
    def call(self, entity: Entity) -> None:
        """
        An abstract method for executing the intent.
        
        params:
        entity (Entity): An entity argument that the intent should execute upon
        
        returns: 
        This methods does not return any value
        """
        pass