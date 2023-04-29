from __future__ import annotations
from abc import abstractclassmethod
from typing.generic import Contact, DateTime, Location, Resolvable, Entity
from typing import Callable, Optional


class AppName(Entity, Resolvable):
    pass


class App(Entity):
    app_name: AppName

    @abstractclassmethod
    def get_predicate(
        App,
        app_name: Optional[AppName] = None,
    ) -> Callable[[App], bool]:
        raise NotImplementedError
