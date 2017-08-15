#from Node2 import Node


class NodePath(list):
    separator = '.'

    @staticmethod
    def join(first, *rest):
        path = NodePath(first)
        for name in rest:
            part = NodePath.cast(name)
            path.extend(part)
        return path

    @staticmethod
    def cast(path):
        """Converts passed argument to NodePath (if needed)"""
        if path is None:
            return NodePath()
        # if isinstance(path, NodePath):
        #     return path
        return NodePath(path)

    # def create_path(root: Node, path) -> Node:
    @staticmethod
    def create_path(root, path):
        # TODO: move somewhere else - this is Node-implementation dependant
        path = NodePath.cast(path)
        if path.is_absolute:
            raise NotImplementedError("Absolute path creation is not implemented")
        if len(path) == 0:
            return root
        node = root.get_node(name=path[0])
        if node is None:
            from contextshell.Node import Node  # TODO: move to the header when Node2 replaces Node
            node = Node()
            root.append(node, path[0])
        return NodePath.create_path(node, path[1:])

    def __init__(self, representation=[], absolute=False):
        super().__init__()
        self.is_absolute = absolute
        if isinstance(representation, int):
            self.append(representation)
        elif isinstance(representation, str):
            self._parse_path(representation)
        elif isinstance(representation, NodePath):
            self.is_absolute = representation.is_absolute
            self.extend(representation)
        elif isinstance(representation, list):
            # TODO: check element's types?
            self.extend(representation)
        else:
            raise ValueError("Could not convert {} to NodePath".format(representation))

    @property
    def base_path(self):
        """Returns sub-path consisting of all but last element"""
        return NodePath(self[:-1])

    @property
    def base_name(self):
        """Returns last path element"""
        return self[-1]

    @staticmethod
    def _to_path_part(name: str):
        """Guess actual path element type"""
        # TODO: is this method really needed? Shouldn't path have opaque elements?
        if name.isnumeric():
            return int(name)
        return name

    def _parse_path(self, text):
        text = text.strip()
        if text.startswith(NodePath.separator):
            self.is_absolute = True
        new_path = map(NodePath._to_path_part, [part for part in text.split(NodePath.separator) if len(part) > 0])
        self.extend(new_path)

    def __str__(self):
        text_representation = NodePath.separator.join(map(str, self))
        if self.is_absolute:
            return NodePath.separator + text_representation
        return text_representation
