from representations.text_tree_builder import TextTreeBuilder


def test01():
    text = "Get directions to the Eagles game if it will be raining"
    builder = TextTreeBuilder(parser_name="stanza")
    tree = builder.build(input=text, rules_enabled=True)
    root_node = tree.root_node

    assert root_node.label == "root"
    assert root_node.children[0].label == "S"
    assert root_node.children[0].children[0].label == "Command"
    assert root_node.children[0].children[0].children[0].label == "Condition"
    assert root_node.children[0].children[0].children[0].children[0].label == "If"
    body_node = root_node.children[0].children[0].children[0].children[0].children[0]
    assert body_node.label == "Body"
    assert body_node.children[0].label == "Command"
    assert body_node.children[0].children[0].label == "Action"
    expected_labels = ["hd", "Arg", "Arg"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                body_node.children[0].children[0].children,
                expected_labels,
            )
        ]
    )
    test_node = root_node.children[0].children[0].children[0].children[0].children[1]
    assert test_node.label == "Test"
    assert test_node.children[0].label == "mark"
    assert test_node.children[1].label == "Command"
    assert test_node.children[1].children[0].label == "Action"
    expected_labels = ["Arg", "aux", "aux", "hd"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                test_node.children[1].children[0].children,
                expected_labels,
            )
        ]
    )


def test02():
    text = "If it will be raining then get directions to the Eagles game"
    builder = TextTreeBuilder(parser_name="stanza")
    tree = builder.build(input=text, rules_enabled=True)
    root_node = tree.root_node

    assert root_node.label == "root"
    assert root_node.children[0].label == "S"
    assert root_node.children[0].children[0].label == "Command"
    assert root_node.children[0].children[0].children[0].label == "Condition"
    assert root_node.children[0].children[0].children[0].children[0].label == "If"

    test_node = root_node.children[0].children[0].children[0].children[0].children[0]
    assert test_node.label == "Test"
    assert test_node.children[0].label == "mark"
    assert test_node.children[1].label == "Command"
    assert test_node.children[1].children[0].label == "Action"
    expected_labels = ["Arg", "aux", "aux", "hd"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                test_node.children[1].children[0].children,
                expected_labels,
            )
        ]
    )

    body_node = root_node.children[0].children[0].children[0].children[0].children[1]
    assert body_node.label == "Body"
    assert body_node.children[0].label == "Command"
    assert body_node.children[0].children[0].label == "Action"
    expected_labels = ["advmod", "hd", "Arg", "Arg"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                body_node.children[0].children[0].children,
                expected_labels,
            )
        ]
    )


def test03():
    text = "Unless there is traffic in the city, tell her I will be on time"
    builder = TextTreeBuilder(parser_name="stanza")
    tree = builder.build(input=text, rules_enabled=True)
    root_node = tree.root_node

    assert root_node.label == "root"
    assert root_node.children[0].label == "S"
    assert root_node.children[0].children[0].label == "Command"
    assert root_node.children[0].children[0].children[0].label == "Condition"
    assert root_node.children[0].children[0].children[0].children[0].label == "If"

    test_node = root_node.children[0].children[0].children[0].children[0].children[0]
    assert test_node.label == "Test"
    assert test_node.children[0].label == "mark"
    assert test_node.children[1].label == "Command"

    punct_node = root_node.children[0].children[0].children[0].children[0].children[1]
    assert punct_node.label == "punct"

    body_node = root_node.children[0].children[0].children[0].children[0].children[2]
    assert body_node.label == "Body"
    assert body_node.children[0].label == "Command"
    assert body_node.children[0].children[0].label == "Action"


def test04():
    text = "If it will be raining then get directions to the Eagles game and tell Jane I may be late"
    builder = TextTreeBuilder(parser_name="stanza")
    tree = builder.build(input=text, rules_enabled=True)
    root_node = tree.root_node

    assert root_node.label == "root"
    assert root_node.children[0].label == "S"
    assert root_node.children[0].children[0].label == "Command"
    assert root_node.children[0].children[0].children[0].label == "Condition"
    assert root_node.children[0].children[0].children[0].children[0].label == "If"

    test_node = root_node.children[0].children[0].children[0].children[0].children[0]
    assert test_node.label == "Test"
    assert test_node.children[0].label == "mark"
    assert test_node.children[1].label == "Command"
    assert test_node.children[1].children[0].label == "Action"
    expected_labels = ["Arg", "aux", "aux", "hd"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                test_node.children[1].children[0].children,
                expected_labels,
            )
        ]
    )

    body_node = root_node.children[0].children[0].children[0].children[0].children[1]
    assert body_node.label == "Body"
    assert body_node.children[0].label == "Command"
    assert body_node.children[0].children[0].label == "Action"
    expected_labels = ["advmod", "hd", "Arg", "Arg"]
    assert all(
        [
            child.label == expected_label
            for (child, expected_label) in zip(
                body_node.children[0].children[0].children,
                expected_labels,
            )
        ]
    )
    assert body_node.children[1].label == "cc"
    assert body_node.children[2].label == "Command_conj"


# def test_condition_basic1():
#     text = "If there is no traffic in the city then tell her I will be on time"
#     tree = Tree(text, parser)
#     assert tree is not None
#     assert tree.root_node.children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].text == 'trigger'
#     assert tree.root_node.children[0].children[0].children[0].text == 'mark'
#     assert tree.root_node.children[0].children[0].children[1].text == 'action:verify'
#     assert tree.root_node.children[0].children[1].text == 'action'
#     assert tree.root_node.children[0].children[1].children[0].text == 'advmod'
#     assert tree.root_node.children[0].children[1].children[1].text == 'action:exec'


# def test_condition_basic2():
#     text = "Provided that there is no traffic in the city, tell her I will be on time"
#     tree = Tree(text, parser)
#     assert tree is not None
#     assert tree.root_node.children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].text == 'trigger'
#     assert tree.root_node.children[0].children[0].children[0].text == 'hd'
#     assert tree.root_node.children[0].children[0].children[1].text == 'mark'
#     assert tree.root_node.children[0].children[0].children[2].text == 'action:verify'
#     assert tree.root_node.children[0].children[1].text == 'punct'
#     assert tree.root_node.children[0].children[2].text == 'action'
#     assert tree.root_node.children[0].children[2].children[0].text == 'action:exec'


# def test_condition_else():
#     text = "Delete all reminders if it rains, otherwise create a reminder"
#     tree = Tree(text, parser)
#     assert tree is not None
#     assert tree.root_node.children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].children[0].text == 'action:exec'
#     assert tree.root_node.children[0].children[1].text == 'trigger'
#     assert tree.root_node.children[0].children[1].children[0].text == 'mark'
#     assert tree.root_node.children[0].children[1].children[1].text == 'action:verify'
#     assert tree.root_node.children[0].children[2].text == 'punct'
#     assert tree.root_node.children[0].children[3].text == 'action:else'
#     assert tree.root_node.children[0].children[3].children[0].text == 'advmod'
#     assert tree.root_node.children[0].children[3].children[1].text == 'action:exec'


# def test_condition_conjoint_action():
#     text = "If I have a meeting now then after you delete the reminder tell me the weather"
#     tree = Tree(text, parser)
#     assert tree is not None
#     assert tree.root_node.children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].text == 'trigger'
#     assert tree.root_node.children[0].children[0].children[0].text == 'mark'
#     assert tree.root_node.children[0].children[0].children[1].text == 'action:verify'
#     assert tree.root_node.children[0].children[1].text == 'action'
#     assert tree.root_node.children[0].children[1].children[0].text == 'action'
#     assert tree.root_node.children[0].children[1].children[0].children[0].text == 'advmod'
#     assert tree.root_node.children[0].children[1].children[0].children[1].text == 'mark'
#     assert tree.root_node.children[0].children[1].children[0].children[2].text == 'action:exec'
#     assert tree.root_node.children[0].children[1].children[1].text == 'action'
#     assert tree.root_node.children[0].children[1].children[1].children[0].text == 'action:exec'


# def test_condition_conjoint_action2():
#     text = "Delete the reminder if I have a meeting now, and tell me the weather"
#     tree = Tree(text, parser)
#     assert tree is not None
#     assert tree.root_node.children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].children[1].text == 'trigger'
#     assert tree.root_node.children[0].children[1].text == 'punct'
#     assert tree.root_node.children[0].children[2].text == 'cc'
#     assert tree.root_node.children[0].children[3].text == 'action'
#     assert tree.root_node.children[0].children[3].children[0].text == 'action:exec'


# def test_condition_ifelse():
#     text = "If there is traffic in the city tell Mary that I will be late, otherwise tell her I will be on time"
#     tree = Tree(text, parser)
#     assert tree is not None
#     assert tree.root_node.children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].text == 'trigger'
#     assert tree.root_node.children[0].children[0].children[0].text == 'mark'
#     assert tree.root_node.children[0].children[0].children[1].text == 'action:verify'
#     assert tree.root_node.children[0].children[1].text == 'action'
#     assert tree.root_node.children[0].children[1].children[0].text == 'action:exec'
#     assert tree.root_node.children[0].children[2].text == 'punct'
#     assert tree.root_node.children[0].children[3].text == 'action:else'
#     assert tree.root_node.children[0].children[3].children[0].text == 'advmod'
#     assert tree.root_node.children[0].children[3].children[1].text == 'action:exec'
