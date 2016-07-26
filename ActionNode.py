from Node import *
from PyNode import *
import functools

class ActionNode(Node):
    ActionNodeName = '@actions'
    def __init__(self, callback = None):
        super().__init__()
        #TODO: check if passed prototype have right signature
        if callback == None:
            callback = self.__call__
        else:
            self.__call__ = callback
        self.value = callback

    def __call__(self, target, *arguments):
        callback = self.value
        if callback == None:
            raise NotImplemented('__call__ method not overriden or no callback provided')
        return callback(self, target, *arguments)

def Action(callback):
    @CreatorFunction
    def action_creator(parent_node : Node):
        if ActionNode.ActionNodeName not in parent_node:
            parent_node.append_node(ActionNode.ActionNodeName, Node())

        commands = parent_node[ActionNode.ActionNodeName]
        commands.append_node(callback.__name__, ActionNode(callback))
    return action_creator

