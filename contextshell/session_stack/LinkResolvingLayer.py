from contextshell.session_stack.CrudSessionLayer import *
from contextshell.ActionNode import ActionNode
from typing import List


class LinkResolvingLayer(CrudSessionLayer):
    """Layer responsible for transparent link nodes handling"""

    def __init__(self):
        super().__init__()

    @property
    def session_actions(self):
        return [LinkCreateAction(), LinkReadAction(), IsLinkAction()]

    def _rewrite_links_in_path(self, path: NodePath) -> NodePath:
        path = NodePath.cast(path)
        if not path.is_absolute:
            raise ValueError("Cannot rewrite relative paths")

        real_path = NodePath(absolute=True)
        for name in path.base_path:
            real_path = NodePath.join(real_path, name)
            if self._is_link(real_path):
                real_path = self._rewrite_link(real_path)
        return NodePath.join(real_path, path.base_name)

    def _rewrite_path(self, path) -> NodePath:
        real_path = self._rewrite_links_in_path(path)
        if self._is_link(real_path):
            return self._rewrite_link(real_path)
        return real_path

    def _rewrite_link(self, path: NodePath) -> NodePath:
        # TODO: handle relative and absolute links?
        assert self.next_layer.exists(path)
        link_path = self.next_layer.get(path)
        assert isinstance(link_path, NodePath)
        return link_path

    def _is_link(self, path: NodePath) -> bool:
        if not self.next_layer.exists(path):
            return False
        node_value = self.next_layer.get(path)
        return isinstance(node_value, NodePath)

    def get(self, path: NodePath):
        return self.next_layer.get(self._rewrite_path(path))

    def set(self, path: NodePath, new_value):
        self.next_layer.set(self._rewrite_path(path), new_value)

    def _rewrite_path_to_link(self, path: NodePath, real_path: NodePath, link_path: NodePath) -> NodePath:
        relative_path = path.relative_to(real_path)
        return NodePath.join(link_path, relative_path)

    def list(self, path: NodePath) -> List[NodePath]:
        real_path = self._rewrite_path(path)
        path_list = self.next_layer.list(real_path)
        path_list = map(lambda p: self._rewrite_path_to_link(p, real_path, path), path_list)
        return list(path_list)

    def exists(self, path: NodePath) -> bool:
        return self.next_layer.exists(self._rewrite_links_in_path(path))

    def create(self, path: NodePath, value=None):
        path = NodePath.cast(path)
        self.next_layer.create(NodePath.join(self._rewrite_path(path.base_path), path.base_name), value)

    def remove(self, path: NodePath):
        # TODO: check removal of .link.node.link
        self.next_layer.remove(self._rewrite_links_in_path(path))


class LinkCreateAction(ActionNode):
    def __init__(self):
        super().__init__(NodePath('create.link'))

    def __call__(self, session: CrudSessionLayer, target: NodePath, *arguments):
        link_path = NodePath.join(target, arguments[0])
        backing_path = NodePath.cast(arguments[1])
        if session.exists(link_path):
            raise RuntimeError(f"{link_path} node already exists")
        session.create(link_path, backing_path)


class LinkReadAction(ActionNode):
    def __init__(self):
        super().__init__(NodePath('link.read'))

    def __call__(self, session: CrudSessionLayer, target: NodePath, *arguments):
        pass


class IsLinkAction(ActionNode):
    def __init__(self):
        super().__init__(NodePath('is.link'))

    def __call__(self, session: CrudSessionLayer, target: NodePath, *arguments):
        assert len(arguments) == 0
        target_value = session.get(target)  # FIXME: get is being redirected to link backing path
        return isinstance(target_value, NodePath)
