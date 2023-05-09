from abc import abstractclassmethod
from typing import List, Optional, List, Union
from entities.generic import *
from entities.shopping import *
from providers.data_model import DataModel


class Shopping:
    @classmethod
    def find_products(
        cls,
        product_name: Optional[ProductName] = None,
        product_attribute: Optional[ProductAttribute] = None,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
    ) -> List[ProductEntity]:
        data_model = DataModel()
        data = data_model.get_data(ProductEntity)
        if product_name:
            data = [x for x in data if x.product_name == product_name]

        if product_attribute:
            data = [x for x in data if x.product_attribute == product_attribute]

        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.date_time in date_time]
            else:
                data = [x for x in data if x.date_time == date_time]

        if location:
            data = [x for x in data if x.location == location]

        return data

    @classmethod
    def find_shopping_lists(
        cls,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
    ) -> List[ShoppingListEntity]:
        data_model = DataModel()
        data = data_model.get_data(ShoppingListEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.date_time in date_time]
            else:
                data = [x for x in data if x.date_time == date_time]

        if location:
            data = [x for x in data if x.location == location]

        return data

    @classmethod
    def add_to_shopping_list(
        cls,
        shopping_list_name: ShoppingListName,
        product_name: Optional[ProductName] = None,
        amount: Optional[Amount] = None,
    ) -> ShoppingListEntity:
        shopping_list = ShoppingListEntity(
            shopping_list_name=shopping_list_name,
            product_name=product_name,
            amount=amount,
        )
        data_model = DataModel()
        data_model.append(shopping_list)
        return shopping_list

    @classmethod
    def order(
        cls,
        product_name: Optional[ProductName] = None,
        product_attribute: Optional[ProductAttribute] = None,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
        amount: Optional[Amount] = None,
    ) -> OrderEntity:
        order = OrderEntity(
            product_name=product_name,
            product_attribute=product_attribute,
            date_time=date_time,
            location=location,
            amount=amount,
        )
        data_model = DataModel()
        data_model.append(order)
        return order
