from abc import abstractclassmethod
from typing import Iterable, Union
from api.v5.exceptions.resolvable import Resolvable
from typing.generic import Entity


class ResponderCommand(Resolvable):
    
    @abstractclassmethod
    def default_responder(cls, response: Union[Iterable[Entity], Entity]):
        raise NotImplementedError
