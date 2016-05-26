from ContextNode import *

class ContextCommand:
    def __init__(self, target : ContextNode, command : ContextNode, arguments):
        self.target = target
        self.command = command
        self.arguments = arguments

    def invoke(self) -> ContextNode:
        evaluated_arguments = []
        for arg in self.arguments:
            if isinstance(arg, ContextNode):
                evaluated_arguments.append(arg)
            else:
                if isinstance(arg, ContextCommand):
                    evaluated_arguments.append(arg.invoke())
                else:
                    try:
                        evaluated_arguments.append(ContextNode(eval(arg)))
                    except NameError:
                        evaluated_arguments.append(str(arg))
        return self.command.call(self.target, evaluated_arguments)

    def __str__(self):
        return "{{{}: {} {}}}".format(self.target, self.command, " ".join(self.arguments))
