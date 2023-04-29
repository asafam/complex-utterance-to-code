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
            data = [x for x in data if x.data.get("product_name") == product_name]

        if product_attribute:
            data = [
                x for x in data if x.data.get("product_attribute") == product_attribute
            ]

        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.data.get("date_time") in date_time]
            else:
                data = [x for x in data if x.data.get("date_time") == date_time]

        if location:
            data = [x for x in data if x.data.get("location") == location]

        return data

    @classmethod
    def find_shopping_lists(
        cls,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
        product_name: Optional[ProductName] = None,
    ) -> List[ShoppingListEntity]:
        data_model = DataModel()
        data = data_model.get_data(ShoppingListEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.data.get("date_time") in date_time]
            else:
                data = [x for x in data if x.data.get("date_time") == date_time]

        if location:
            data = [x for x in data if x.data.get("location") == location]

        if product_name:
            data = [x for x in data if x.data.get("product_name") == product_name]

        return data

    @classmethod
    def add_product_to_shopping_list(
        cls,
        shopping_list: ShoppingListEntity,
        product_name: Optional[ProductName] = None,
    ) -> List[ShoppingListEntity]:
        data_model = DataModel()
        data = data_model.get_data(ShoppingListEntity)
        if shopping_list:
            data = [x for x in data if x.data.get("shopping_list") == shopping_list]

        if product_name:
            data = [x for x in data if x.data.get("product") == product_name]

        return data

    @classmethod
    def create_order(
        cls,
        products: Optional[Union[ProductEntity, List[ProductEntity]]],
    ) -> OrderEntity:
        order = OrderEntity(products=products)
        data_model = DataModel()
        data_model.append(order)
        return order
