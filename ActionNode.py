from Node import Node


class ActionNode(Node):
    ActionsNodeName = '@actions'

    def __init__(self, callback=None):
        # TODO: check if passed prototype have right signature
        if callback is not None:
            self.__call__ = callback
        super().__init__(callback)

    def __call__(self, target: Node, *arguments):
        callback = self.get()
        if callback is None:
            raise NotImplementedError('__call__ method not overridden or no callback provided')
        return callback(target, *arguments)
