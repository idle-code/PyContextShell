import unittest

from PyNode import *
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

class AttributeNodeTests(unittest.TestCase):
    def setUp(self):
        self.node = CustomNode()

    def test_attribute_node_get(self):
        self.assertTrue('@readonly_attribute' in self.node)

        self.assertEqual(3412, self.node['@readonly_attribute'].value)

    def test_attribute_node_set(self):
        self.assertTrue('@attribute' in self.node)

        self.assertEqual(None, self.node['@attribute'].value)
        self.node['@attribute'].value = "spam"
        self.assertEqual("spam", self.node['@attribute'].value)

    @unittest.skip("attribute rewrite is required for it to work")
    def test_attribute_property_get(self):
        self.assertTrue('@readonly_attribute' in self.node)

        self.assertEqual(3412, self.node.readonly_attribute)

    @unittest.skip("attribute rewrite is required for it to work")
    def test_attribute_property_set(self):
        self.assertTrue('@attribute' in self.node)

        self.assertEqual(None, self.node.attribute)
        self.node.attribute = 123
        self.assertEqual(123, self.node.attribute)

if __name__ == '__main__':
    unittest.main()

