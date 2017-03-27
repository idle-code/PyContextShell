from ActionNode import ActionNode
from Node2 import Node


class ArgumentError(Exception):
    pass


class GetAction(ActionNode):
    def __call__(self, target: Node, *arguments):
        if len(arguments) > 0:
            raise ArgumentError("get action doesn't expect any arguments")
        return target.get()


class SetAction(ActionNode):
    def __call__(self, target: Node, *arguments):
        if len(arguments) != 1:
            raise ArgumentError("Expected single argument, got {}".format(len(arguments)))
        new_value = arguments[0]
        target.set(new_value)


class ListAction(ActionNode):
    def __call__(self, target: Node, *arguments):
        if len(arguments) > 0:
            raise ArgumentError("list action doesn't expect any arguments")
        return target.list()


class RemoveAction(ActionNode):
    def __call__(self, target: Node, *arguments):
        if len(arguments) != 1:
            raise ArgumentError("remove action expect single arguments")
        name_to_remove = arguments[0]
        #target.remove(name_to_remove)
