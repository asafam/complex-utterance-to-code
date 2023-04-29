from abc import abstractclassmethod
from typing import Iterable, Union, Optional
from api.v5.exceptions.resolvable import Resolvable
from typing.generic import Entity
from typing.timer import Timer


class TimerCommand(Resolvable):
    
    @abstractclassmethod
    def pause(
        cls,
        timer: Optional[Timer] = None,
    ) -> bool:
        raise NotImplementedError

    @abstractclassmethod    
    def restart(
        cls,
        timer: Optional[Timer] = None,
    ) -> bool:
        raise NotImplementedError

    @abstractclassmethod
    def stop(
        cls,
        timer: Optional[Timer] = None,
    ) -> bool:
        raise NotImplementedError
