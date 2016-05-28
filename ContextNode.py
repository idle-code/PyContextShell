from NodePath import *
import collections

class ContextNode:
    def __init__(self, value = None): #TODO: add parent parameter
        self._value = value
        self._subnodes = []
        #self._parent = parent

    @property
    def parent(self):
        return self._parent

    def get(self):
        return self._value

    def set(self, new_value):
        self._value = new_value

    def create(self, name, node):
        print("Creating {} = {}".format(name, node))
        if not isinstance(node, ContextNode):
            node = ContextNode(node)
        if self.get_subnode(name) != None:
            raise NameError(str(name) + ' already exists')
        self._subnodes.append((name, node))

    def delete(self, name):
        node_to_delete = self.get_subnode(name)
        del self._subnodes[self._subnodes.index(node_to_delete)]

    def contains(self, name):
        return name in self

    def __contains__(self, name):
        return self.get_subnode_entry(name) != None

    def __iter__(self):
        return map(lambda t: t[1], self._subnodes)

    def __len__(self):
        return len(self._subnodes)

    def __getattr__(self, name):
        return self.get_subnode(name)

    #def __setattr__(self, name, value):
    #    if not name.startswith('_'):
    #        self.create(name, value)

    def __delattr__(self, name):
        self.delete(name)

    def __setitem__(self, name, value):
        if name in self:
            self[name].set(value)
        else:
            self.create(name, value)

    def __getitem__(self, name):
        subnode = self.get_subnode(name)
        if subnode == None:
            raise KeyError("Couln't find subnode: '{}'".format(name))
        return subnode

    def __str__(self):
        return str(self.get())

    def get_subnode(self, name): #TODO: replace by path
        subnode = self.get_subnode_entry(name)
        if subnode == None:
            #TODO: throw an exception?
            return None
        return subnode[1]

    def get_subnode_entry(self, name):
        if name == None:
            return self
        if isinstance(name, int):
            if name < len(self._subnodes):
                return self._subnodes[name]
            else:
                return None
        return next((n for n in self._subnodes if n[0] == name), None)

    # For debug purposes
    def print(self, prefix = ''):
        print('{}:\t{}'.format(prefix, self))
        for sub in self._subnodes:
            sub[1].print(NodePath.separator.join([prefix, sub[0]]))


