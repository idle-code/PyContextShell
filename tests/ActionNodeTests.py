import unittest

from PyNode import *
from ActionNode import *

class CustomNode(PyNode):
    def __init__(self):
        super().__init__()
        self.simple_value = "simple_action"

    @Action
    def simple_action(self, target : Node, *args : [Node]):
        if not isinstance(target, Node):
            raise TypeError('target is required to be Node but is ' + repr(target))

        for arg in args:
            if not isinstance(arg, Node):
                raise TypeError('arguments are required to be Node but one is ' + repr(arg))

        return self.simple_value

    #@Action('named')
    #def simple_named_action(self, target : Node, *args : [Node]):
    #    if not isinstsance(target, Node):
    #        raise TypeError('target is required to be Node but is ' + type(target))

    #    for arg in args:
    #        if not isinstsance(arg, Node):
    #            raise TypeError('arguments are required to be Node but onee is ' + type(arg))

    #    return "named_action"

class ActionNodeTests(unittest.TestCase):
    def setUp(self):
        self.node = CustomNode()

    def test_simple_action(self):
        self.assertTrue('@actions' in self.node)

        actions_node = self.node['@actions']
        self.assertTrue('simple_action' in actions_node)

        simple_action_node = actions_node['simple_action']
        self.assertEqual("simple_action", simple_action_node(self.node))
        self.assertEqual("simple_action", simple_action_node(self.node, Node(1), Node("test"), Node(None)))
        self.assertEqual("simple_action", simple_action_node(self.node, 1, "test", None))

    def test_simple_method(self):
        self.assertTrue(hasattr(self.node, 'simple_action'))

        self.assertEqual("simple_action", self.node.simple_action(self.node))
        self.assertEqual("simple_action", self.node.simple_action(self.node, Node(1), Node("test"), Node(None)))
        self.assertEqual("simple_action", self.node.simple_action(self.node, 1, "test", None))

if __name__ == '__main__':
    unittest.main()

