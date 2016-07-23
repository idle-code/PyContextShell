
class NodePath(list):
    separator = '.'
    def __init__(self, representation = None, absolute = False):
        super(NodePath, self).__init__()
        self.isabsolute = absolute
        if isinstance(representation, str):
            self._parse_path(representation)
        elif isinstance(representation, list):
            self.extend(representation)

    @property
    def branch_name(self):
        return str(NodePath(self[:-1]))

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

