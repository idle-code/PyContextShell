import unittest

from PyNode import *
from ActionNode import *
from AttributeNode import *

class CustomNode(PyNode):
    def __init__(self):
        super().__init__()
        self.attribute_value = None

    @Action
    def simple_action(self, target : Node):
        return [target]

    @Attribute
    def readonly_attribute(self):
        return 3412

    @Attribute
    def attribute(self):
        return self.attribute_value

    @attribute.setter
    def attribute_setter(self, new_value):
        self.attribute_value = new_value


class PyNodeTests(unittest.TestCase):
    def setUp(self):
        self.node = CustomNode()

    def test_action_decorator_node(self):
        self.assertTrue('@actions' in self.node)
        commands_node = self.node['@actions']
        self.assertTrue('simple_action' in commands_node)

        simple_action_node = commands_node['simple_action']
        self.assertIn(self.node, simple_action_node(self.node))

    #FIXME
    @unittest.skip("method/function rewrite is required for it to work")
    def test_action_decorator_method(self):
        self.assertTrue('@actions' in self.node)
        commands_node = self.node['@actions']
        self.assertTrue('simple_action' in commands_node)

        self.assertIn(self.node, self.node.simple_action(self.node))

    def test_attribute_decorator_node_get(self):
        self.assertTrue('@readonly_attribute' in self.node)

        self.assertEqual(3412, self.node['@readonly_attribute'].value)

    def test_attribute_decorator_node_set(self):
        self.assertTrue('@attribute' in self.node)

        self.assertEqual(None, self.node['@attribute'].value)
        self.node['@attribute'].value = "spam"
        self.assertEqual("spam", self.node['@attribute'].value)

    #FIXME
    @unittest.skip("attribute rewrite is required for it to work")
    def test_attribute_decorator_property_get(self):
        self.assertTrue('@readonly_attribute' in self.node)

        self.assertEqual(3412, self.node.readonly_attribute)

    #FIXME
    @unittest.skip("attribute rewrite is required for it to work")
    def test_attribute_decorator_property_set(self):
        self.assertTrue('@attribute' in self.node)

        self.assertEqual(None, self.node.attribute)
        self.node.attribute = 123
        self.assertEqual(123, self.node.attribute)


if __name__ == '__main__':
    unittest.main()
