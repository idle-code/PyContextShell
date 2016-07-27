from Node import *

def CreatorFunction(creator_function):
    creator_function.is_creator = True
    return creator_function

def is_creator(function):
    return hasattr(function, 'is_creator')

class PyNode(Node):
    def __init__(self):
        super().__init__()
        self._populate_subnodes()

    def _populate_subnodes(self):
        for field_name, field in type(self).__dict__.items():
            if not is_creator(field):
                continue
            #print("Creating node for:", field_name)
            original_field = field(self)
            setattr(self, field_name, original_field)

