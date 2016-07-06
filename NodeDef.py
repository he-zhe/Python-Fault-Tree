class Node:

    def __init__(self, name, logic, init_state=False):
        self.name = name
        self.logic = logic
        if logic == 'OR':
            self.logic_func = lambda x, y: x or y
        elif logic == 'AND':
            self.logic_func = lambda x, y: x and y
        else:
            raise ValueError('logic can be only "and" or "or"')
        self.children = []
        self.state = init_state  # Ture or False
        self.parent = None

    def get_name(self):
        return self.name

    def calculate_state(self):
        if self.is_leaf():
            return self.state
        result = self.children[0].get_state()
        for child in self.children:
            result = self.logic_func(result, child.state)
        self.state = result
        return self.state

    def get_state(self):
        return self.state

    def change_state(self, new_state):
        self.state = new_state

    def add_child(self, new_child):
        if not isinstance(new_child, Node):
            raise TypeError("{} is not an instance of Node".format(new_child))
        self.children.append(new_child)
        new_child.parent = self

    def is_leaf(self):
        return not bool(self.children)

    def is_root(self):
        return not bool(self.parent)

    def update_all_from_leaf(self):
        if self.is_leaf():
            self.calculate_state()
        for child in self.children:
            child.update_all_from_leaf()
        self.calculate_state()

    def propagate_up(self):
        walk = self
        while not walk.is_root():
            walk.calculate_state()
            walk = walk.parent
        walk.calculate_state()
