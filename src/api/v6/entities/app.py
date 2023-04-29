from __future__ import annotations
from entities.entity import Entity
from entities.resolvable import Resolvable


class AppName(Entity, Resolvable):
    pass


class App(Entity):
    app_name: AppName
