class Node:

    def __init__(self, name, logic='AND', init_state=False):
        if type(name) is not str:
            raise TypeError("name can only be string type")
        self.name = name

        if logic.upper() == 'OR' or logic.upper() == 'AND':
            self.logic = logic.upper()
        else:
            raise TypeError('logic can be only "AND" or "OR"')

        if type(init_state) is not bool:
            raise TypeError("State can only be booleen type")
        self.state = init_state  # Ture or False
        self.children = []

    # calculate state based on its immediate children alone.
    def calculate_state(self):
        if self.is_leaf():
            return self.state

        if self.logic == 'OR':  # OR gate, not leaf
            self.state = any(child.state for child in self.children)
        elif self.logic == 'AND':  # AND gate, not leaf
            self.state = all(child.state for child in self.children)
        else:
            raise TypeError('logic can be only "AND" or "OR"')
        return self.state

    def change_state(self, new_state):
        if type(new_state) is not bool:
            raise TypeError("State can only be booleen type")
        self.state = new_state

    def add_child(self, new_child):
        if not isinstance(new_child, Node):
            raise TypeError("The node to be added is not an instance of Node")
        self.children.append(new_child)

    def is_leaf(self):
        return not bool(self.children)

    # Update the tree based on all leaves
    # This can be implemented in stack instead of recursion, if large tree.
    def update_all_from_leaf(self):
        if self.is_leaf():
            return

        stack = [self]
        visitd = {self.name: False}

        while stack:
            last_node = stack[-1]
            # Leaf, or one's children already add to stack
            if visitd[last_node.name]:
                last_node.calculate_state()
                stack.pop()
            else:
                visitd[last_node.name] = True
                for child in last_node.children:
                    if not child.is_leaf():
                        stack.append(child)
                        visitd[child.name] = False
        #  Recursive implementation
        # if self.is_leaf():
        #     self.calculate_state()
        #     return
        # for child in self.children:
        #     child.update_all_from_leaf()
        # self.calculate_state()
