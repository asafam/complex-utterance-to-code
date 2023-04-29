from entities.resolvable import Resolvable
from entities.entity import Entity


class Album(Entity, Resolvable):
    pass


class Artist(Entity, Resolvable):
    pass


class Genre(Entity, Resolvable):
    pass


class MusicType(Entity, Resolvable):
    pass


class MusicEntity(Entity, Resolvable):
    pass


class Playlist(Entity, Resolvable):
    pass


class Song(Entity, Resolvable):
    pass