from __future__ import annotations
from abc import abstractmethod
from document import Doc


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
