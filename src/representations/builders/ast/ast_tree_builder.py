import ast
from representations.tree.node import Node
from representations.tree.tree import Tree
from representations.builders.base_tree_builder import BaseTreeBuilder
from representations.builders.ast.builders.builder_factory import BuilderFactory
from representations.builders.ast.tearers.tearer_factory import TearerFactory


class ASTTreeBuilder(BaseTreeBuilder):
    def __init__(self) -> None:
        super().__init__()

    def build(self, input, rules_enabled=False) -> Tree:
        tree = Tree(input=input)
        tree.root_node = self._build_tree(input)

        # if rules_enabled:
        #     tree = self.apply_rules(
        #         tree=tree, rules_file_path="config/representations/ast_rules.yaml"
        #     )

        return tree

    def tear(self, tree: Tree) -> str:
        factory = TearerFactory()
        tearer = factory.get_tearer()
        module = ast.Module(
            body=[tearer.tear(child) for child in tree.root_node.children]
        )
        return module

    def _build_tree(self, input: str) -> Node:
        root_node = Node("root")

        asdl = ast.parse(input)
        factory = BuilderFactory()
        builder = factory.get_builder(asdl)
        node = builder.build(asdl)

        root_node.add_child(node)

        # tearer = TearerFactory().get_tearer(node)
        # asdl2 = tearer.tear(node)
        # x = ast.unparse(asdl2)
        # print(x)
        
        return root_node
