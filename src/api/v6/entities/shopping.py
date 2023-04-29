from entities.resolvable import Resolvable
from entities.entity import Entity


class OrderEntity(Entity, Resolvable):
    pass


class Product(Entity, Resolvable):
    pass


class ProductAttribute(Entity, Resolvable):
    pass


class ProductEntity(Entity, Resolvable):
    pass


class ShoppingListEntity(Entity, Resolvable):
    pass
