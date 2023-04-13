from rules.node_rule import NodeRule
from representations.tree.node import Node
import copy
from utils.text_utils import is_node_condition, is_node_condition_nested_action


class ActionExecNodeRule(NodeRule):
    def run_rule(self, root_node, tree):
        super().run_rule(root_node, tree)

        if root_node.text not in ["action", "trigger", "action:else"]:
            return

        action_exec_node = Node(text="action:exec")
        action_verify_node = Node(text="action:verify")

        if root_node.text == "trigger":
            self.build_action_verify_node(
                action_verify_node, root_node, root_node.children
            )
        elif root_node.text in ["action", "action:else"]:
            self.build_action_exec_node(action_exec_node, root_node, root_node.children)

        for action_sub_node in [action_exec_node, action_verify_node]:
            if len(action_sub_node.children) == 1:
                action_sub_node_idx = root_node.children.index(action_sub_node)
                insert_idx = max(action_sub_node_idx, 0)
                children = action_sub_node.children[0].children
                action_sub_node.set_children(children)
                children_copy = copy.copy(children)
                for child_node in children_copy:
                    if child_node.text in ["punct", "cc"]:
                        parent_insert_idx = root_node.parent.children.index(root_node)
                        root_node.parent.insert_child(parent_insert_idx, child_node)
                    if child_node.text in ["mark", "advmod"]:
                        root_node.insert_child(insert_idx, child_node)
                        insert_idx += 1

    def build_action_verify_node(
        self, action_verify_node, root_node, children, insert_idx=0
    ):
        children_copy = copy.copy(children)
        for child_node in children_copy:
            if is_node_condition_nested_action(child_node):
                if child_node.text in ["ccomp"]:
                    if child_node.children[0].text in ["mark", "obj"]:
                        root_node.insert_child(insert_idx, child_node.children[0])
                        insert_idx += 1

                    if not action_verify_node.parent:
                        root_node.insert_child(insert_idx, action_verify_node)
                        insert_idx += 1

                    action_verify_node.add_child(child_node)
                else:
                    insert_idx += 1
            elif child_node.text in ["punct", "cc"]:
                parent_insert_idx = root_node.parent.children.index(root_node)
                root_node.parent.insert_child(parent_insert_idx, child_node)
                insert_idx += 1
            elif child_node.text not in ["mark", "aux"]:
                if not action_verify_node.parent:
                    root_node.insert_child(insert_idx, action_verify_node)
                    insert_idx += 1

                action_verify_node.add_child(child_node)
            else:
                insert_idx += 1

    def build_action_exec_node(
        self, action_exec_node, root_node, children, insert_idx=0
    ):
        children_copy = copy.copy(children)
        for child_node in children_copy:
            if child_node.text in ["punct", "cc"]:
                parent_insert_idx = root_node.parent.children.index(root_node)
                root_node.parent.insert_child(parent_insert_idx, child_node)
            elif child_node.text not in [
                "action",
                "action:else",
                "trigger",
            ] and child_node.text not in ["mark", "advmod"]:
                if not action_exec_node.parent:
                    root_node.insert_child(insert_idx, action_exec_node)
                    insert_idx += 1

                action_exec_node.add_child(child_node)
            else:
                insert_idx += 1
