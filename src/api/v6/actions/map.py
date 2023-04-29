from abc import abstractclassmethod
from typing import List, Union, Optional
from entities.resolvable import Resolvable
from entities.generic import *
from entities.map import *
from providers.data_model import DataModel


class Map:
    @classmethod
    def find_on_map(cls, location: Location) -> List[MapEntity]:
        data_model = DataModel()
        data = data_model.get_data(MapEntity)
        if location:
            data = [x for x in data if x.data.get("location") == location]

        return data
