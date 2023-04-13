from rules.node_rule import NodeRule
from representations.tree.node import Node


class ActionNodeRule(NodeRule):
    def run_rule(self, root_node, tree):
        super().run_rule(root_node, tree)

        if root_node.text != "root":
            return

        action_node = Node(text="action")
        action_node.set_children(root_node.children)
        root_node.set_children([action_node])

        for root_node in tree.extra_root_nodes:
            action_node = Node(text="action")
            action_node.set_children(root_node.children)
            root_node.add_child(action_node)

        # if len(tree.root_nodes) > 1:
        #     for i, root_node in enumerate(tree.root_nodes):
        #         if i > 0:
        #             tree.root_nodes.add_child(root_node.children[0]) # add the root -> [action] of each consequent node under the first root node
