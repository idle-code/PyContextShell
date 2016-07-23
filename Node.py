from NodePath import *
import collections

class Node:
    def __init__(self, value = None):
        self._value = value
        self._subnodes = []
        self._parent = self

    @property
    def parent(self):
        return self._parent

    @property
    def name(self):
        if self.parent == self:
            return ""
        # Find node by reference
        #parent_node_entry = self.parent.get_subnode_entry_by_reference(self)
        #if parent_node_entry == None:
        #    raise NameError('Could not find name for node {} ({})'.format(repr(self), str(self)))

        this_node_name = next((n[0] for n in self.parent._subnodes if n[1] is self), None)
        if this_node_name == None:
            raise NameError('Could not find name for node {} ({})'.format(repr(self), str(self)))
        return this_node_name

    @property
    def path(self):
        if self.parent == self:
            return str(NodePath(absolute = True))
        this_node_path = NodePath(self.parent.path)
        this_node_path.append(self.name)
        return str(this_node_path)

    def get(self):
        return self._value

    def set(self, new_value):
        self._value = new_value

    def create(self, name, node):
        if not isinstance(node, Node):
            node = Node(node)
        if self.get_subnode(name) != None:
            raise NameError(str(name) + ' already exists')
        node._parent = self
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

    def __repr__(self):
        value = self.get()
        return "{{{} = {}}}".format(self.path, type(value))

    def get_subnode(self, name): #TODO: replace by path
        subnode = self.get_subnode_entry(name)
        if subnode != None:
            return subnode[1]
        subnode = self.get_object_entry(name)
        if subnode != None:
            return subnode[1]

        return None

    def get_subnode_entry(self, name):
        if name == None:
            return self
        if isinstance(name, int):
            if name < len(self._subnodes):
                return self._subnodes[name]
            else:
                return None
        return next((n for n in self._subnodes if n[0] == name), None)

    def get_object_entry(self, name):
        if name == None:
            return self
        if not name.startswith('@'):
            return None

        # Find property named 'name' in this object
        field = getattr(self, name[1:]) # strip '@' at begining
        if field == None:
            return None

        if isinstance(field, Node): #TODO: check if this is necessarry
            return (name, field)
        else:
            temporary_node = Node(field)
            # FIXME: get temporary/attribute nodes properly anchored
            # temporary_node._parent = self
            return (name, temporary_node) # CHECK: how to store fractal data in properties? Is it needed for such properties?

    # For debug purposes
    def print(self, prefix = ''):
        print('{}:\t{}'.format(prefix, self))
        for sub in self._subnodes:
            sub[1].print(NodePath.separator.join([prefix, sub[0]]))


