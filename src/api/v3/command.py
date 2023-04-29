from __future__ import annotations
from typing import Mapping
from abc import abstractmethod
from entity import Entity
from query import Query
from span import Span


class Command:
    """
    Command class
    """

    def __init__(self, doc: Doc):
        """
        The class constructor that takes a <a href='query.html>Query</a> that should yield the concrete command instance.

        params:
        query (Query): A user query

        returns:
        A Command instance
        """
        pass

    @abstractmethod
    def call(self, params: Params) -> None:
        """
        An abstract method for executing the intent.

        params:
        entity (Entity): An entity argument that the intent should execute upon

        returns:
        This methods does not return any value
        """
        pass

    @abstractmethod
    def get_params(self, value_mappings: Mapping[Span, Entity]) -> Params:
        """
        An abstract method that returns an EntityDescriptor for the model. Given a query this method is
        responsible for inferring the EntityDescriptor. Additional information and value mapping is provided
        via the value mappings variable to this method.

        params:
        query (Query): A user query
        value_mapping (Mapping[Span, Entity]): Optional variable that allows the mapping of spans within a query to Entity values

        returns:
        An EntityDescriptor object for this model
        """
        pass
