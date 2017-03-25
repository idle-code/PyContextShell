class Node:
    def __init__(self, value=None):
        self._value = value
        self._subnodes = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.value is not None and type(self.value) != type(new_value):
            raise TypeError("Value have different type ({}) than node ({})".format(type(new_value), type(self.value)))
        self._value = new_value

    @property
    def subnodes(self):
        return list(map(lambda p: p[1], self._subnodes))

    def append(self, name: str, node):
        if name is None:
            raise NameError("Invalid appended node name - None")
        if node is None:
            raise ValueError("Cannot append None node")
        if self.get_node(name) is not None:
            raise NameError("Node '{}' already exists".format(name))
        self._subnodes.append((name, node))

    def get_node(self, name: str=None):
        for p in self._subnodes:
            if p[0] == name:
                return p[1]
        return None

    def remove(self, name: str=None):
        node_to_remove = self.get_node(name=name)
        if node_to_remove is None:
            raise NameError("Node '{}' doesn't exists".format(name))
        self._subnodes = [p for p in self._subnodes if p[0] != name]
        return node_to_remove

    def exists(self, name: str=None) -> bool:
        return self.get_node(name=name) is not None
