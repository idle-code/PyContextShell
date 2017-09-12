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
        names = map(lambda p: p[0], self._subnodes)
        index = 0
        indexed_names = []
        for n in names:
            indexed_names.append(n if n is not None else index)
            index += 1
        return indexed_names

    def append(self, node, name: str=None):
        """Append provided node as subnode"""
        if node is None:
            raise ValueError("Cannot append None node")
        if name is not None:
            if len(name) == 0:
                raise NameError("Invalid appended node name - empty")
            if self.get_node(name) is not None:
                raise NameError("Node '{}' already exists".format(name))
        node._parent = self
        self._subnodes.append((name, node))

    def get_node(self, name: str=None, index: int=None) -> 'Node':
        """Return subnode with provided name"""
        if name is not None:
            for p in self._subnodes:
                if p[0] == name:
                    return p[1]
        elif index is not None:
            if 0 <= index < len(self._subnodes):
                return self._subnodes[index][1]
        else:
            raise NameError("No name or index provided")
        return None

    def __getitem__(self, name_or_index) -> 'Node':
        if isinstance(name_or_index, int):
            node = self.get_node(index=name_or_index)
        else:
            node = self.get_node(name=name_or_index)
        if node is None:
            raise KeyError(name_or_index)
        return node

    def remove(self, name: str=None, index=None) -> 'Node':
        """Remove subnode with provided name"""
        node_to_remove = self.get_node(name=name, index=index)
        if node_to_remove is None:
            raise NameError("Node '{}' doesn't exists".format(name))
        self._subnodes = [p for p in self._subnodes if p[1] is not node_to_remove]
        return node_to_remove

    def contains(self, name: str=None, index: int=None) -> bool:
        """Check if there is a subnode with provided name"""
        return self.get_node(name=name, index=index) is not None

    # def __contains__(self, name: str):
    #     return self.contains(name=name)
