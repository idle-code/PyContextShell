import unittest

from PyNode import *
from ActionNode import *
from AttributeNode import *

class CustomNode(PyNode):
    def __init__(self):
        super().__init__()
        self.attribute_value = None

    @Attribute
    def readonly_attribute(self):
        return 3412

    @Attribute
    def attribute(self):
        return self.attribute_value

    @attribute.setter
    def attribute_setter(self, new_value):
        self.attribute_value = new_value

    @VirtualNode(name='@virtual_attribute')
    def virtual_attribute(self):
        if isinstance(self.parent.value, int):
            return self.parent.value + 1
        return 1

    @VirtualNode
    def virtual(self):
        if isinstance(self.parent.value, str):
            return self.parent.value + "bar"
        return "ra"

class PyNodeTests(unittest.TestCase):
    def setUp(self):
        self.node = CustomNode()

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

    @unittest.skip("Re-check if needed/valid")
    def test_virtual_attribute(self):
        self.assertEqual(1, self.node.virtual_attribute())

        self.assertTrue('@virtual_attribute' in self.node)
        virtual_node = self.node['@virtual_attribute']
        self.assertIsInstance(virtual_node, Node)
        self.assertEqual(1, virtual_node.value)

        self.assertTrue('@virtual_attribute' in virtual_node)
        virtual_node = virtual_node['@virtual_attribute']
        self.assertIsInstance(virtual_node, Node)
        self.assertEqual(2, virtual_node.value)

    def test_virtual_node(self):
        self.assertEqual("ra", self.node.virtual())

        self.assertTrue('virtual' in self.node)
        virtual_node = self.node['virtual']
        self.assertIsInstance(virtual_node, Node)
        self.assertEqual("ra", virtual_node.value)

        self.assertTrue('virtual' in virtual_node)
        virtual_node = virtual_node['virtual']
        self.assertIsInstance(virtual_node, Node)
        self.assertEqual("rabar", virtual_node.value)

if __name__ == '__main__':
    unittest.main()

