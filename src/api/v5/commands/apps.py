from abc import abstractclassmethod
from typing import Iterable, Union, Optional
from api.v5.exceptions.resolvable import Resolvable
from typing.generic import Entity
from typing.apps import App


class AppsCommand(Resolvable):
    
    @abstractclassmethod
    def open(
        app: Optional[App] = None,
    ) -> bool:
        raise NotImplementedError

