
class NodePath(list):
    separator = '.'
    def __init__(self, representation = None):
        super(NodePath, self).__init__()
        self.isabsolute = False
        if isinstance(representation, str):
            self._parse_path(representation)
        if isinstance(representation, list):
            self.clear()
            self.extend(representation)

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

