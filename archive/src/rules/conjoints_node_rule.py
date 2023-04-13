from representations.tree.node import Node
from rules.node_rule import NodeRule
import copy
from utils.text_utils import has_conjunction, is_node_condition


class ConjointsNodeRule(NodeRule):
    def run_rule(self, root_node, tree):
        super().run_rule(root_node, tree)

        self.add_conjoints_nodes(root_node, root_node.children)

    def add_conjoints_nodes(
        self, root_node, children, insert_idx=None, rebuild_origin_node=True
    ):
        if root_node.text not in ["action", "action:else", "trigger"] and not (
            root_node.text in ["ccomp"]
            and root_node.parent.text in ["action", "action:else", "trigger"]
        ):
            return

        if not has_conjunction(root_node, children):
            return

        node_text = root_node.text.split(":")[0]
        node = None
        conjoint_node = None
        insert_idx = insert_idx or 0
        child_hd_idx = next((i for i, n in enumerate(children) if n.text == "hd"), -1)

        children_copy = copy.copy(children)
        for i, child_node in enumerate(children_copy):
            if child_node.text in ["conj", "advcl"] and not is_node_condition(
                child_node
            ):
                conjoint_node = (
                    node if (node and i < child_hd_idx) else Node(text=node_text)
                )
                if not conjoint_node.parent:
                    root_node.insert_child(insert_idx, conjoint_node)
                    insert_idx += 1
                conjoint_node.add_child(child_node)
            elif rebuild_origin_node:
                node = (
                    node if (node and node != conjoint_node) else Node(text=node_text)
                )
                if not node.parent:
                    root_node.insert_child(insert_idx, node)
                    insert_idx += 1
                node.add_child(child_node)

                if child_node.text in ["ccomp", "xcomp"]:
                    self.add_conjoints_nodes(
                        root_node,
                        child_node.children,
                        insert_idx=insert_idx,
                        rebuild_origin_node=False,
                    )
