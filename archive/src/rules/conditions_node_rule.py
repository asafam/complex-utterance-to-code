from utils.text_utils import is_node_condition
from rules.node_rule import NodeRule
from representations.tree.node import Node
import copy
from utils.text_utils import (
    has_condition,
    has_condition_else,
    has_condition_nested_action,
    is_node_conjunction,
    is_node_condition_simple,
    is_node_condition_nested_action,
    is_node_condition_else,
)


class ConditionsNodeRule(NodeRule):
    ###
    #   if
    #   if else
    #   if if if
    #   if if if else
    ###

    def run_rule(self, root_node, tree):
        super().run_rule(root_node, tree)
        self.add_conditions_nodes(root_node, root_node.children)

    def add_conditions_nodes(
        self, root_node, children, insert_idx=0, force_condition=False
    ):
        if not root_node.text in ["action", "action:else", "trigger"]:
            return

        condition = has_condition(root_node) and not root_node.text == "trigger"
        condition_nested_action = (
            has_condition_nested_action(root_node) and not root_node.text == "trigger"
        )
        condition_else = has_condition_else(root_node)
        if not force_condition and not (
            condition or condition_nested_action or condition_else
        ):
            return

        condition_node_idx = next(
            (i for i, n in enumerate(children) if is_node_condition(n)), -1
        )
        conjunction_node_idx = next(
            (i for i, n in enumerate(children) if is_node_conjunction(n)), -1
        )
        conjoint_after_condition = (
            condition_node_idx < conjunction_node_idx
            and condition_node_idx != 0
            and conjunction_node_idx != -1
        )
        if conjoint_after_condition:
            return

        action_node = Node(text="action")
        trigger_node = Node(text="trigger")
        insert_idx = insert_idx or 0

        children_copy = copy.copy(children)
        for child_node in children_copy:
            if is_node_condition_nested_action(child_node):
                if not trigger_node.parent:
                    root_node.insert_child(insert_idx, trigger_node)
                    insert_idx += 1

                trigger_node.add_child(child_node)
            elif is_node_condition_simple(child_node):
                if not trigger_node.parent:
                    root_node.insert_child(insert_idx, trigger_node)
                    trigger_node.set_children(child_node.children)
                    child_node.detach()
                    insert_idx += 1
            elif is_node_condition_else(child_node):
                action_else_node = Node(text="action:else")
                action_else_node.set_children(child_node.children)
                action_parent = child_node.get_parent("action")
                child_node.detach()
                # add trigger as a sibling to action
                action_parent.add_child(action_else_node)
            elif child_node.parent.text not in ["trigger"]:
                if not action_node.parent:
                    root_node.insert_child(insert_idx, action_node)
                    insert_idx += 1

                action_node.add_child(child_node)

        # for child_node in children_copy:
        #     if is_node_condition_else(child_node):
        #         action_else_node = Node(text='action:else')
        #         action_else_node.set_children(child_node.children)
        #         action_parent = child_node.get_parent('action')
        #         child_node.detach()
        #         # add trigger as a sibling to action
        #         action_parent.add_child(action_else_node)
        #         # insert_idx += 1
        #     # elif nestedprovided that it rains then remind me to bring an umbrellad_node.children[-1].detach()
        #     elif is_node_condition(child_node):
        #         trigger_node = Node(text='trigger')
        #         # move the condition functional node under it
        #         trigger_node.set_children(child_node.children)
        #         child_node.detach()
        #         # add trigger as a sibling to action
        #         root_node.insert_child(insert_idx, trigger_node)
        #         insert_idx += 1
        #     elif not has_condition_else(child_node):
        #         # set the action node
        #         if not action_node.parent:
        #             root_node.insert_child(insert_idx, action_node)
        #             insert_idx += 1
        #         # add nodes under action node
        #         if nested_action and child_node.text in ['parataxis' , 'advcl']:
        #            action_node.set_children(child_node.children)
        #            child_node.detach()
        #         else:
        #             action_node.add_child(child_node)
        #     else:
        #         insert_idx += 1
