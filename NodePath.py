
class NodePath(list):
    separator = '.'

    @staticmethod
    def join(*names):
        path = NodePath()
        for name in names:
            name = NodePath.cast(name)
            path.extend(name)
        return path

    @staticmethod
    def cast(path):
        """If needed converts passed argument to NodePath"""
        if isinstance(path, NodePath):
            return path
        return NodePath(path)

    def __init__(self, representation = [], absolute = False):
        super().__init__()
        self.isabsolute = absolute
        if isinstance(representation, str):
            self._parse_path(representation)
        elif isinstance(representation, list):
            self.extend(representation)
        else:
            raise ValueError("Could not convert {} to NodePath".format(representation))

    @property
    def base_path(self):
        return NodePath(self[:-1])

    @property
    def base_name(self):
        return str(NodePath(self[-1]))

    def _parse_path(self, text):
        self.clear()
        text = text.strip()
        if text.startswith(NodePath.separator):
            self.isabsolute = True
        new_path = [part for part in text.split(NodePath.separator) if len(part) > 0]
        self.extend(new_path)

    def __str__(self):
        text_representation = NodePath.separator.join(self)
        if self.isabsolute:
            return NodePath.separator + text_representation
        return text_representation

