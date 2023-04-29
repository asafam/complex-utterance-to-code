
from __future__ import annotations
from abc import abstractclassmethod, abstractmethod


class Entity:
    
    def __init__(self, **kwargs) -> None:
        super().__init__()
        kwargs = {**{'value': kwargs.get('text')}, **kwargs}
        self.data = kwargs
            
        
    @abstractmethod
    def __gt__(self, other) -> bool:
        raise NotImplementedError()
    
    def __str__(self) -> str:
        return self.data.get('text')