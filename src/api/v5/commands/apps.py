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
