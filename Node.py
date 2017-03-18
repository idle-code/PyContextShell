from NodePath import *
import types


class Node:
    @staticmethod
    def cast(value):
        if isinstance(value, Node):
            return value
        return Node(value)

    def __init__(self, value=None):
        self._parent = None
        self._value = value
        self._subnodes = []

        #self.append_node_generator('@parent', lambda: self.parent)
        self.append_node_generator('@name', lambda parent_node: parent_node.name)
        self.append_node_generator('@path', lambda parent_node: parent_node.path)
        self.append_node_generator('@index', lambda parent_node: parent_node.index)

    @property
    def parent(self):
        return self._parent

    @property
    def name(self):
        if self.parent is None:
            return None

        # Workaround for virtual nodes (which are not found in parent subnodes)
        if Node.is_virtual(self):
            return self._virtual_name

        # Find node name searching parent subnodes for instance:
        this_node_name = self.parent._get_subnode_by_reference(self)

        if this_node_name is None:
            raise NameError('Could not find name for node {} ({})'.format(repr(self), str(self)))
        return this_node_name

    @property
    def index(self):
        if not self.parent:
            return None
        return self.parent._get_subnode_index_by_name(self.name)

    @staticmethod
    def is_virtual(node):
        return hasattr(node, '_virtual_name')

    @property
    def path(self):
        if self.parent is None:
            return str(NodePath(absolute=True))
        this_node_path = NodePath.join(self.parent.path, self.name)
        return str(this_node_path)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self.value is not None and type(self.value) != type(new_value):
            raise TypeError("Value have different type ({}) than node ({})".format(type(new_value), type(self.value)))
        self._value = new_value

    def append_node(self, path: NodePath, node):
        if not isinstance(node, Node):
            raise TypeError("Could not add non-Node class")

        path = NodePath.cast(path)
        parent_node = self[path.base_path]
        parent_node._add_subnode(path.base_name, node)
        node._parent = self

    def replace_node(self, path : NodePath, new_node):
        path = NodePath.cast(path)
        parent_node = self[path.base_path]
        return parent_node._replace_subnode(path.base_name, new_node)

    def append_node_generator(self, path : NodePath, generator):
        if not isinstance(generator, types.FunctionType):
            raise TypeError("Could not add non-callable node generator")

        path = NodePath.cast(path)
        parent_node = self[path.base_path]
        parent_node._add_subnode(path.base_name, generator)

    def remove_node(self, path : NodePath):
        path = NodePath.cast(path)
        parent_node = self._get_subnode_by_path(path.base_path)
        if not parent_node:
            return False
        parent_node._remove_subnode(path.base_name)
        return True

    def create_path(self, path : NodePath):
        path = NodePath.cast(path)
        current_node = self
        for name in path:
            if name not in current_node.subnode_names:
                current_node.append_node(name, Node())
            current_node = current_node._get_subnode_by_name(name)
        return current_node

    def __contains__(self, path : NodePath):
        path = NodePath.cast(path)
        parent_node = self._get_subnode_by_path(path.base_path)
        if not parent_node:
            return False
        return path.base_name in parent_node.subnode_names

    def __getitem__(self, path : NodePath):
        target_node = self._get_subnode_by_path(NodePath.cast(path))
        if not target_node:
            raise NameError("Could not find path: {}".format(path))
        return target_node

    def __str__(self):
        return str(self.value)

    @property
    def subnode_names(self):
        return list(map(lambda entry: entry[0], self._subnodes))

    @property
    def subnodes(self):
        return list(map(lambda entry: self._get_subnode_by_name(entry[0]), self._subnodes))

    def _add_subnode(self, name : str, node):
        if not isinstance(name, str):
            raise TypeError("Node name is not string")
        if name in self.subnode_names:
            raise NameError("Subnode entry with name '" + str(name) + "' already exists")

        #print("Creating node: '{}' - {}".format(name, type(name)))
        self._subnodes.append((name, node))

    def _replace_subnode(self, existing_name: str, new_node):
        if not isinstance(existing_name, str):
            raise TypeError("Existing node name is not string")
        subnode_index = self._get_subnode_index_by_name(existing_name)
        if subnode_index is None:
            raise NameError("Subnode entry with name '" + str(existing_name) + "' doesn not exists")

        if isinstance(new_node, Node):
            # Take subs from replaced node into new one:
            existing_node = self._subnodes[subnode_index][1]
            if isinstance(existing_node, Node):
                # Take subnodes from replaced node into new_node:
                new_node._subnodes = existing_node._subnodes
                for entry in new_node._subnodes:
                    if not isinstance(entry[1], types.FunctionType): # if subnode is generator
                        # Update subnode subnodes with new parent:
                        entry[1]._parent = new_node
                    #CHECK: find a way to preserve nodes and generators from new_node
                existing_node._parent = None
                existing_node._subnodes = []

            new_node._parent = self

        self._subnodes[subnode_index] = (existing_name, new_node)

    def _remove_subnode(self, name : str):
        if name not in self.subnode_names:
            raise NameError("Subnode entry with name '" + str(name) + "' does not exists")
        # Filter-out requested subnode
        self._subnodes = [n for n in self._subnodes if not n[0] == name]

    def _get_subnode_by_path(self, path : NodePath):
        path = NodePath.cast(path)
        if len(path) == 0:
            return self

        next_node = self._get_subnode_by_name(path.pop(0))
        if next_node is None:
            return None

        return next_node._get_subnode_by_path(path)

    def _get_subnode_by_name(self, name : str): #TODO: replace by path
        subnode = None
        if isinstance(name, str):
            subnode = next((n[1] for n in self._subnodes if n[0] == name), None)
        elif isinstance(name, int):
            index = name
            if index < 0 or index >= len(self._subnodes):
                return None
            subnode = self._subnodes[index][1]

        if subnode is None:
            return None

        if isinstance(subnode, types.FunctionType): # if subnode is generator
            #print("Instantiating '{}' virtual node (in {})".format(name, self.path))
            subnode = subnode(self)
            if not isinstance(subnode, Node):
                #print("Wrapping '{}' value into node".format(subnode))
                subnode = Node(subnode)
            subnode._parent = self
            subnode._virtual_name = name
            return subnode
        elif isinstance(subnode, Node):
            return subnode
        raise TypeError('Unknown subnode type: ' + type(subnode))

    def _get_subnode_by_reference(self, reference):
        return next((n[0] for n in self._subnodes if n[1] is reference), None)

    def _get_subnode_index_by_reference(self, reference):
        return next((index for index, value in enumerate(self._subnodes) if value[1] is reference), None)

    def _get_subnode_index_by_name(self, name):
        return next((index for index, value in enumerate(self._subnodes) if value[0] == name), None)
