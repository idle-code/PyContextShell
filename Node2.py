class Node:
    def __init__(self, value=None):
        self._value = value
        self._subnodes = []
        self._parent = None

    @property
    def parent(self):
        """Return parent of this node"""
        return self._parent

    def get(self):
        """Get value stored in this node"""
        return self._value

    def set(self, new_value):
        """Store provided value in this node"""
        if type(self._value) != type(new_value):
            raise TypeError("Value have different type ({}) than node ({})".format(type(new_value), type(self._value)))
        self._value = new_value

    def list(self):
        """List names of the subnodes"""
        return list(map(lambda p: p[0], self._subnodes))

    def append(self, name: str, node):
        """Append provided node as subnode"""
        if name is None:
            raise NameError("Invalid appended node name - None")
        if len(name) == 0:
            raise NameError("Invalid appended node name - empty")
        if node is None:
            raise ValueError("Cannot append None node")
        if self.get_node(name) is not None:
            raise NameError("Node '{}' already exists".format(name))
        node._parent = self
        self._subnodes.append((name, node))

    def get_node(self, name: str):
        """Return subnode with provided name"""
        for p in self._subnodes:
            if p[0] == name:
                return p[1]
        return None

    def __getitem__(self, name: str):
        node = self.get_node(name=name)
        if node is None:
            raise KeyError(name)
        return node

    def remove(self, name: str):
        """Remove subnode with provided name"""
        node_to_remove = self.get_node(name=name)
        if node_to_remove is None:
            raise NameError("Node '{}' doesn't exists".format(name))
        self._subnodes = [p for p in self._subnodes if p[0] != name]
        return node_to_remove

    def contains(self, name: str) -> bool:
        """Check if there is a subnode with provided name"""
        return self.get_node(name=name) is not None

    # def __contains__(self, name: str):
    #     return self.contains(name=name)
