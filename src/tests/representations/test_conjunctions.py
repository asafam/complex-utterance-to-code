# from parsers import factory
# from tree.tree import Tree


# parser = factory.create_parser(pname='stanza')
    

# def test_conjunction_single():
#     text = "Delete all reminders and snooze the alarm"
#     tree = Tree(text, parser)
#     assert tree is not None
#     assert tree.root_node.children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].children[0].text == 'action:exec'
#     assert tree.root_node.children[0].children[0].children[0].children[0].text == 'hd'
#     assert tree.root_node.children[0].children[0].children[0].children[1].text == 'obj'
#     assert tree.root_node.children[0].children[1].text == 'cc'
#     assert tree.root_node.children[0].children[2].text == 'action'
#     assert tree.root_node.children[0].children[2].children[0].text == 'action:exec'
    

# def test_conjunction_single():
#     text = "After you delete all reminders, snooze the alarm"
#     tree = Tree(text, parser)
#     assert tree is not None
#     assert tree.root_node.children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].text == 'action'
#     assert tree.root_node.children[0].children[0].children[0].text == 'mark' # After
#     assert tree.root_node.children[0].children[0].children[1].text == 'action:exec'
#     assert tree.root_node.children[0].children[0].children[1].children[0].text == 'nsubj'   # you
#     assert tree.root_node.children[0].children[0].children[1].children[1].text == 'hd'      # delete
#     assert tree.root_node.children[0].children[0].children[1].children[2].text == 'obj'     # all reminders
#     assert tree.root_node.children[0].children[1].text == 'punct'
#     assert tree.root_node.children[0].children[2].text == 'action'
#     assert tree.root_node.children[0].children[2].children[0].text == 'action:exec'
    
