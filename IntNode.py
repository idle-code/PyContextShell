from ActionNode import *


class IntNode(PyNode):
    def __init__(self, value=0):
        super().__init__(value)
        if not isinstance(value, int):
            raise TypeError("Int node can only store integer values")

    @Action
    def set(self, target_node, new_value):
        if not isinstance(new_value.value, int):
            raise TypeError("Int node can only store integer values")

        new_value = new_value.value

        if '@minimum' in target_node.subnode_names:
            minimum = target_node['@minimum'].value
            if new_value < minimum:
                raise ValueError("Could not set value below minimum: {}".format(minimum))

        if '@maximum' in target_node.subnode_names:
            maximum = target_node['@maximum'].value
            if new_value > maximum:
                raise ValueError("Could not set value below maximum: {}".format(maximum))

        target_node.value = new_value
