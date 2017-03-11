from ActionNode import *


class VirtualNode(PyNode):
    def __init__(self, getter, setter=None):
        super().__init__()
        if not hasattr(getter, '__call__'):
            raise TypeError("VirtualNode require functional getter not {}".format(repr(getter)))
        self._getter = getter

        if setter is not None and not hasattr(setter, '__call__'):
            raise TypeError("VirtualNode require functional setter not {}".format(repr(getter)))
        self._setter = setter

    @property
    def value(self):
        return self._getter()

    @value.setter
    def value_set(self, new_value):
        if self._setter is None:
            raise TypeError("No setter defined for virtual node")
        return self._setter(new_value)

