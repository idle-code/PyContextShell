from NodePath import *
import collections

class ContextNode:
    def __init__(self, value = None):
        self._value = value
        self._subnodes = []

    def get(self):
        return self._value

    def set(self, new_value):
        self._value = new_value

    def create(self, name, node):
        if not isinstance(node, ContextNode):
            node = ContextNode(node)
        if self._get_subnode(name) != None:
            raise NameError(str(name) + ' already exists')
        self._subnodes.append((name, node))

    def delete(self, name):
        node_to_delete = self._get_subnode(name)
        del self._subnodes[self._subnodes.index(node_to_delete)]

    def contains(self, name):
        return self._get_subnode_entry(naem) != None

    def _get_subnode(self, name):
        subnode = self._get_subnode_entry(name)
        if subnode == None:
            #TODO: throw an exception?
            return None
        return subnode[1]

    def _get_subnode_entry(self, name):
        if name == None:
            return self
        if isinstance(name, int):
            if name < len(self._subnodes):
                return self._subnodes[name]
            else:
                return None
        return next((n for n in self._subnodes if n[0] == name), None)

    def __getattr__(self, name):
        return self._get_subnode(name)

    def __getitem__(self, name):
        if isinstance(name, NodePath): #TODO: fix when using bare list
            if len(name) > 0:
                n = name.pop(0)
                return self._get_subnode(n)[name]
            else:
                return self
        return self._get_subnode(name)

    def __str__(self):
        return str(self.get())

    def print(self, prefix = ''):
        print('{}:\t{}'.format(prefix, self.get()))
        for sub in self._subnodes:
            sub[1].print(NodePath.separator.join([prefix, sub[0]]))


