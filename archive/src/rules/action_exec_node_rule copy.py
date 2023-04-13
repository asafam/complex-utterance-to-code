from rules.node_rule import NodeRule
from representations.tree.node import Node
import copy


class ActionExecNodeRule(NodeRule):
    def run_rule(self, root_node, tree):
        super().run_rule(root_node, tree)

        if root_node.text not in ["action", "trigger", "action:else"]:
            return

        action_node = Node(text="action:exec")
        insert_idx = 0

        children_copy = copy.copy(root_node.children)
        for child_node in children_copy:
            if child_node.text not in ["punct", "action", "trigger", "action:else"]:
                if (
                    root_node.text == "trigger"
                    and child_node.text not in ["mark", "punct"]
                ) or (
                    root_node.text in ["action", "action:else"]
                    and child_node.text not in ["mark", "punct", "cc"]
                ):
                    # set the action node
                    if not action_node.parent:
                        root_node.insert_child(insert_idx, action_node)

                    action_node.add_child(child_node)
            insert_idx += 1
