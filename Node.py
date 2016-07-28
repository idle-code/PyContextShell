from NodePath import *
import collections
import functools
import types

class Node:
    def __init__(self, value = None):
        self._parent = self
        self._value = value
        self._subnodes = []

        self.append_node_generator('@parent', lambda: self.parent)
        self.append_node_generator('@name', lambda: self.name)
        self.append_node_generator('@path', lambda: self.path)

    @property
    def parent(self):
        return self._parent

    @property
    def name(self):
        if self.parent is self:
            return ""

        this_node_name = next((n[0] for n in self.parent._subnodes if n[1] is self), None)
        if this_node_name == None:
            # Workaround for wirtual nodes (which are not found in _subnodes)
            if hasattr(self, '_virtual_name'):
                this_node_name = self._virtual_name
            else:
                raise NameError('Could not find name for node {} ({})'.format(repr(self), str(self)))
        return this_node_name

    @property
    def path(self):
        if self.parent == self:
            return str(NodePath(absolute = True))
        this_node_path = NodePath(self.parent.path)
        this_node_path.append(self.name)
        return str(this_node_path)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def append_node(self, name, node):
        if not isinstance(node, Node):
            raise TypeError("Could not add non-Node class")
        node._parent = self
        self._add_subnode(name, node)

    def append_node_generator(self, name, generator):
        if not isinstance(generator, types.FunctionType):
            raise TypeError("Could not add non-callable node generator")
        self._add_subnode(name, generator)

    def remove_node(self, name):
        if name not in self:
            return False
        self._remove_subnode(name)
        return True

    @property
    def _subnode_names(self):
        return map(lambda entry: entry[0], self._subnodes)

    def _add_subnode(self, name, node):
        if name in self._subnode_names:
            raise NameError("Subnode entry with name '" + str(name) + "' already exists")
        self._subnodes.append((name, node))

    def _remove_subnode(self, name):
        if name not in self._subnode_names:
            raise NameError("Subnode entry with name '" + str(name) + "' does not exists")
        self._subnodes = [n for n in self._subnodes if not n[0] == name]

    def get_subnode(self, name): #TODO: replace by path
        if name == None: #TODO: check if this is usefull
            return None
        subnode = next((n[1] for n in self._subnodes if n[0] == name), None)
        if subnode == None:
            return None

        if isinstance(subnode, types.FunctionType): # if subnode is generator
            #print("Instantiating '{}' virtual node".format(name))
            subnode = subnode()
            if not isinstance(subnode, Node):
                #print("Wrapping '{}' value into node".format(subnode))
                subnode = Node(subnode)
                subnode._parent = self
                subnode._virtual_name = name
            return subnode
        elif isinstance(subnode, Node):
            return subnode
        raise TypeError('Unknown subnode type: ' + type(subnode))

    # For debug purposes
    def print(self, prefix = ''):
        print('{}:\t{}'.format(prefix, self))
        for sub in self._subnodes:
            sub[1].print(NodePath.separator.join([prefix, sub[0]]))

    #def contains(self, name):
    #    return name in self

    def __contains__(self, name):
        return name in self._subnode_names

    #def __iter__(self):
    #    return map(lambda t: t[1], self._subnodes)

    def __len__(self):
        return len(self._subnodes)

    #TODO: test
    def __getattr__(self, name):
        #TODO: throw NameError (or similar) when there is no node
        subnode = self.get_subnode(name)
        if subnode == None:
            raise KeyError("Could not find subnode: '{}'".format(name))
        return subnode

    #def __setattr__(self, name, value):
    #    if not name.startswith('_'):
    #        self.create(name, value)

    #def __delattr__(self, name):
    #    self.delete(name)

    #def __setitem__(self, name, value):
    #    if name in self:
    #        self[name].set(value)
    #    else:
    #        self.create(name, value)

    def __getitem__(self, name):
        if isinstance(name, int): # for iteration over nodes:
            subnode = self._subnodes[name]
            return self.get_subnode(subnode[0])

        return getattr(self, name)

    def __str__(self):
        return str(self.value)

    #def __repr__(self):
    #    value = self.value
    #    return "{{{} = {}}}".format(self.path, type(value))


