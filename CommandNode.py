from ContextNode import *

class CommandNode(ContextNode):
    def __init__(self, callback = None):
        super(CommandNode, self).__init__()
        if callback == None:
            callback = self.__call__
        else:
            self.__call__ = callback
        self.set(callback)

    def __call__(self, target, *arguments):
        callback = self.get()
        if callback == None:
            raise NotImplemented('__call__ method not overriden or callback not provided')
        return callback(self, target, arguments)

