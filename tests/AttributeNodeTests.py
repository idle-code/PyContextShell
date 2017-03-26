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


class AttributeNodePythonUsageTests(unittest.TestCase):
    """Methods decorated with @Attribute decorator should behave like normal properties"""

    def setUp(self):
        self.node = CustomNode()

    @unittest.skip("attribute rewrite is required for it to work")
    def test_getter(self):
        self.assertEqual(3412, self.node.readonly_attribute)

    @unittest.skip("attribute rewrite is required for it to work")
    def test_setter(self):
        self.assertIsNone(self.node.attribute)
        self.node.attribute = 1234
        self.assertEqual(1234, self.node.attribute)


class AttributeNodeTests(unittest.TestCase):
    """Methods decorated with @Attribute decorator are visible as attribute nodes"""

    def setUp(self):
        self.node = CustomNode()

    @unittest.skip("Re-write Attribute class or use alternative")
    def test_attribute_node_get(self):
        self.assertTrue(self.node.contains('@readonly_attribute'))

        self.assertEqual(3412, self.node['@readonly_attribute'].value)

    @unittest.skip("Re-write Attribute class or use alternative")
    def test_attribute_node_set(self):
        self.assertTrue(self.node.contains('@attribute'))

        self.assertIsNone(self.node['@attribute'].value)
        self.node['@attribute'].value = "spam"
        self.assertEqual("spam", self.node['@attribute'].value)


if __name__ == '__main__':
    unittest.main()
