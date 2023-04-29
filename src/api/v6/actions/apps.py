from abc import abstractclassmethod
from typing import List, Union, Optional
from entities.resolvable import Resolvable
from entities.generic import Entity
from entities.app import App


class Apps(Resolvable):
    @abstractclassmethod
    def open(
        cls,
        app: Optional[App] = None,
    ) -> bool:
        raise NotImplementedError
