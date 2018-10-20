class NodePath(list):
    # CHECK: if this class could be replaced by build-in os.path
    separator = "."

    @staticmethod
    def join(first, *rest) -> "NodePath":
        path = NodePath(first)
        for name in rest:
            part = NodePath.cast(name)
            path.extend(part)
        return path

    @staticmethod
    def cast(path) -> "NodePath":
        """Converts passed argument to NodePath (if needed)"""
        # TODO: remove this method - be aware what types are passed instead
        if path is None:
            return NodePath()
        return NodePath(path)

    @staticmethod
    def from_python_name(name: str) -> "NodePath":
        name = name.lstrip("_").replace("_", NodePath.separator)
        return NodePath.cast(name)

    def to_python_name(self) -> str:
        name = str(self)
        name = name.lstrip(NodePath.separator).replace(NodePath.separator, "_")
        return name

    def __init__(self, representation=None, absolute=False):
        super().__init__()
        self.is_absolute = absolute
        if isinstance(representation, int):
            self.append(representation)
        elif isinstance(representation, str):
            self._parse_path(representation)
        elif isinstance(representation, NodePath):
            self.is_absolute = representation.is_absolute
            self.extend(representation)
        elif isinstance(representation, (list, tuple)):
            # TODO: check element's types?
            # TODO: is it ever used?
            self.extend(representation)
        elif representation is None:
            pass
        else:
            raise ValueError(f"Could not convert {representation} to NodePath")

    @property
    def is_relative(self) -> bool:
        return not self.is_absolute

    @property
    def is_attribute(self) -> bool:
        if not isinstance(self.base_name, str):
            return False
        return self.base_name.startswith("@")

    @property
    def base_path(self):
        """Returns sub-path consisting of all but last element"""
        return NodePath(self[:-1], absolute=self.is_absolute)

    @property
    def base_name(self):
        """Returns last path element"""
        if not self:
            return None
        return self[-1]

    def is_parent_of(self, other: "NodePath") -> bool:
        """Checks if provided path prefix matches self"""
        other = NodePath.cast(other)
        if self.is_absolute != other.is_absolute:
            raise ValueError(f"Cannot compare absolute and relative paths: {self} and {other}")
        return NodePath(other[: len(self)], absolute=other.is_absolute) == self

    def relative_to(self, other) -> "NodePath":
        """Make current path relative to provided one by removing common prefix"""
        if not other.is_parent_of(self):
            raise ValueError(f"{self} is not relative to {other}")
        return NodePath(self[len(other) :], absolute=False)

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
        non_empty_path_parts = [part for part in text.split(NodePath.separator) if part]
        new_path = map(NodePath._to_path_part, non_empty_path_parts)
        self.extend(new_path)

    def __eq__(self, other):
        other = NodePath.cast(other)
        return self.is_absolute == other.is_absolute and self[:] == other[:]

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        text_representation = NodePath.separator.join(map(str, self))
        if self.is_absolute:
            return NodePath.separator + text_representation
        return text_representation

    def __hash__(self):
        return str(self).__hash__()

    def __repr__(self):
        return f"NodePath('{self}', absolute={self.is_absolute})"
