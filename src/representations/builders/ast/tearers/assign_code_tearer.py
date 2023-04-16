from typing import Any
import re
import ast
from ast import *
from representations.tree.node import Node
from representations.builders.ast.tearers.base_tearer import BaseTearer
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class AssignTearer(BaseTearer):
    def is_match(self, node):
        return re.match(r".+ [\+-\/\*]*= .+", node.label)

    def get_priority(self) -> int:
        return super().get_priority() + 2

    def tear(self, node: Node) -> Any:
        ast_item = ast.parse(node.label)
        value = ast_item.body[0]
        return value
