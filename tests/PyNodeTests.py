import unittest
from PyNode import PyNode


class CustomNode(PyNode):
    def __init__(self):
        super().__init__()
        self._simple_value = 300

    @property
    def simple_property(self):
        return self._simple_value * 2

    @simple_property.setter
    def simple_property(self, new_value):
        self._simple_value = new_value

    def simple_method(self):
        return self._simple_value


class PropertyAccessTests(unittest.TestCase):
    """Check that properties with @node decorator are still
    usable as normal properties"""
    def setUp(self):
        self.node = CustomNode()

    def test_get_simple_property(self):
        self.assertEqual(600, self.node.simple_property)

    def test_set_simple_property(self):
        self.node.simple_property = 100
        self.assertEqual(200, self.node.simple_property)

    def test_simple_method(self):
        self.assertEqual(300, self.node.simple_method())


class NodeAccessTests(unittest.TestCase):
    """Check that properties with @node decorator are visible as nodes"""
    def setUp(self):
        self.node = CustomNode()

    @unittest.skip("Enable when @node decorator is available")
    def test_get_simple_property(self):
        self.assertTrue(self.node.contains('simple_property'))
        self.assertEqual(600, self.node['simple_property'].value)

    @unittest.skip("Enable when @node decorator is available")
    def test_set_simple_property(self):
        self.node['simple_property'].value = 100
        self.assertEqual(200, self.node['simple_property'].value)

if __name__ == '__main__':
    unittest.main()
