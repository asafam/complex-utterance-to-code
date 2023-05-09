from entities.resolvable import Resolvable
from entities.entity import Entity


class OrderEntity(Entity, Resolvable):
    pass


class ProductName(Entity, Resolvable):
    pass


class ProductAttribute(Entity, Resolvable):
    pass


class ProductEntity(Entity, Resolvable):
    pass


class ShoppingListName(Entity, Resolvable):
    pass


class ShoppingListEntity(Entity, Resolvable):
    pass
