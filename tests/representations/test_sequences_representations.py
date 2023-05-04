from representations.builders.lang.text_tree_builder import TextTreeBuilder


def test01():
    text = "Directions to the Eagles game, and to the pharmacy"
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
    expected_labels = ["nmod", "punct", "cc", "nmod_conj"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                root_node.children[0].children[0].children[0].children[1].children,
                expected_labels,
            )
        ]
    )


def test02():
    text = "Directions to the Eagles game and to the pharmacy"
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
    expected_labels = ["nmod", "cc", "nmod_conj"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                root_node.children[0].children[0].children[0].children[1].children,
                expected_labels,
            )
        ]
    )


def test03():
    text = "Directions to the Eagles game, to the Knicks game, and to the pharmacy"
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
    expected_labels = ["nmod", "punct", "cc", "nmod_conj", "punct", "cc", "nmod_conj"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                root_node.children[0].children[0].children[0].children[1].children,
                expected_labels,
            )
        ]
    )
