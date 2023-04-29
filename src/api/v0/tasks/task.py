from abc import abstractclassmethod
from __future__ import annotations


class Task:
    
    @abstractclassmethod
    def find(cls) -> list:
        pass
    
    @abstractclassmethod
    def filter(cls, ) -> list:
        pass
    
    @abstractclassmethod
    def call(cls) -> Entity:
        pass
        