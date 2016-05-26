from ContextNode import *

class CommandNode(ContextNode):
    def __init__(self, callback):
        super(CommandNode, self).__init__()
        self.create('function', callback)

    def call(self, target, parameters):
        return (self.function.get())(target, parameters)
