from Node import Node
from NodePath import NodePath


class ActionNode(Node):
    def __init__(self, path, callback=None):
        # TODO: check if passed prototype have right signature
        if callback is not None:
            self.__call__ = callback
        super().__init__(callback)

        if path is None:
            raise ValueError("Action have to have a path")
        self._path = NodePath.cast(path)
        if self._path.is_absolute:
            raise ValueError("Node path cannot be absolute")
        self._populate_subnodes()

    @property
    def path(self) -> NodePath:
        return self._path

    def _populate_subnodes(self):
        for field_name, field in type(self).__dict__.items():
            if isinstance(field, ActionNode):
                # TODO: check if this binding is correct for other fields
                unbound_method = field.get()
                bound_method = unbound_method.__get__(self, ActionNode)
                new_action = ActionNode(field.path, bound_method)
                setattr(self, field_name, new_action)
                # Create subnode for sub-action:
                action_parent = NodePath.create_path(self, field.path.base_path)
                action_parent.append(new_action, field.path.base_name)

    def __call__(self, target: Node, *arguments):
        callback = self.get()
        if callback is None:
            raise NotImplementedError('__call__ method not overridden or no callback provided')
        return callback(target, *arguments)


def action(function_to_wrap=None, path=None):
    if path is None:
        path = function_to_wrap.__name__

    def action_with_path(callback):
        return ActionNode(path=path, callback=callback)

    if function_to_wrap is None:
        return action_with_path
    else:
        return action_with_path(function_to_wrap)
