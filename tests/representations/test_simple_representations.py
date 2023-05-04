from representations.builders.lang.text_tree_builder import TextTreeBuilder


def test01():
    text = "Directions to the Eagles game"
    builder = TextTreeBuilder(parser_name="stanza")
    tree = builder.build(input=text, rules_enabled=True)
    root_node = tree.root_node

    assert root_node.label == "root"
    assert len(root_node.children) == 1
    assert root_node.children[0].label == "S"
    assert root_node.children[0].children[0].label == "Command"
    assert root_node.children[0].children[0].children[0].label == "Action"
    assert root_node.children[0].children[0].children[0].children[0].label == "hd"
    assert root_node.children[0].children[0].children[0].children[1].label == "Arg"
    assert (
        root_node.children[0].children[0].children[0].children[1].children[0].label
        == "nmod"
    )


def test02():
    text = "I need you to give me directions to the Eagles game"
    builder = TextTreeBuilder(parser_name="stanza")
    tree = builder.build(input=text, rules_enabled=True)
    root_node = tree.root_node

    assert root_node.label == "root"
    assert len(root_node.children) == 1
    assert root_node.children[0].label == "S"
    assert root_node.children[0].children[0].label == "Command"
    assert root_node.children[0].children[0].children[0].label == "Action"
    expected_labels = ["Arg", "hd", "Arg", "xcomp"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                root_node.children[0].children[0].children[0].children, expected_labels
            )
        ]
    )
    xcomp_node = root_node.children[0].children[0].children[0].children[3]
    assert xcomp_node.children[0].label == "mark"
    assert xcomp_node.children[1].label == "Command"
    assert xcomp_node.children[1].children[0].label == "Action"
    expected_labels = ["hd", "iobj", "Arg", "Arg"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                xcomp_node.children[1].children[0].children,
                expected_labels,
            )
        ]
    )
