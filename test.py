from NodeDef import Node

"""
            root(or)
            /       \
    child_1(and)     child_2
    /     \
child_1_1 child_1_2


"""


root = Node('root', 'or')

child_1 = Node('child1', 'and')
child_2 = Node('child2', 'or')

child_1_1 = Node('child_1_1', 'and')
child_1_2 = Node('child_1_1', 'and')


root.add_child(child_1)
root.add_child(child_2)
child_1.add_child(child_1_1)
child_1.add_child(child_1_2)

assert root.children == [child_1, child_2]
assert root.is_root() is True
assert child_1.is_root() is False
assert child_2.is_leaf() is True
assert root.get_name() == 'root'
assert child_1.parent == root
assert child_2.state is False

#  test propagate_up and OR gate
child_2.change_state(True)
assert child_2.state is True
assert root.state is False
child_2.propagate_up()
assert root.state is True

#  test propagate_up and AND gate
assert child_1.state is False
child_1_2.change_state(True)
assert child_1_2.state is True
child_1_2.propagate_up()
assert child_1.state is False


#  test update_all_from_leaf
child_1.change_state(True)
child_2.change_state(False)
child_1_1.change_state(True)
child_1_2.change_state(False)
root.change_state(True)

root.update_all_from_leaf()

assert root.state is False
assert child_1.state is False
assert child_2.state is False
