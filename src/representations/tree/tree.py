from __future__ import annotations


class Tree:
    def __init__(self, input) -> None:
        self.input = input
        self.root_node = None
        self.extra_root_nodes = []

    def __repr__(self) -> str:
        return self.root_node

    def __str__(self) -> str:
        return str(self.root_node)
