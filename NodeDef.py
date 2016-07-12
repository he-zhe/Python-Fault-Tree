class Node:

    def __init__(self, name, logic='AND', init_state=False):
        if type(name) is not str:
            raise TypeError("name can only be string type")
        self.name = name

        if logic == 'OR' or logic == 'AND':
            self.logic = logic
        else:
            raise TypeError('logic can be only "AND" or "OR"')

        if type(init_state) is not bool:
            raise TypeError("State can only be booleen type")
        self.state = init_state  # Ture or False
        self.children = []
        self.parents = []

    # calculate state based on its immediate children alone.
    def calculate_state(self):
        if self.is_leaf():
            return self.state

        if self.logic == 'OR':  # OR gate, not leaf
            self.state = any(child.state for child in self.children)
        else:  # AND gate, not leaf
            self.state = all(child.state for child in self.children)
        return self.state

    def change_state(self, new_state):
        if type(new_state) is not bool:
            raise TypeError("State can only be booleen type")
        self.state = new_state

    def add_child(self, new_child):
        if not isinstance(new_child, Node):
            raise TypeError("The node to be added is not an instance of Node")
        self.children.append(new_child)
        new_child.parents.append(self)

    def is_leaf(self):
        return not bool(self.children)

    def is_root(self):
        return not bool(self.parents)

    # Update the tree based on all leaves
    # This can be implemented in stack instead of recursion, if large tree.
    def update_all_from_leaf(self):
        stack = [self]
        visitd = [False]

        while stack:
            last_node = stack[-1]
            # Leaf, or one's children already add to stack
            if last_node.is_leaf() or visitd[-1]:
                last_node.calculate_state()
                stack.pop()
                visitd.pop()
            else:
                visitd[-1] = True
                for child in last_node.children:
                    stack.append(child)
                    visitd.append(False)
        #  Recursive implementation
        # if self.is_leaf():
        #     self.calculate_state()
        #     return
        # for child in self.children:
        #     child.update_all_from_leaf()
        # self.calculate_state()

    # Update the ancesters of this node, without recalculate the whole tree.
    # Useful when update one or a few node(s).
    def propagate_up(self):
        walks = [self]
        while walks:
            new_walks = []
            for walk in walks:
                walk.calculate_state()
                new_walks += walk.parents
            walks = new_walks
