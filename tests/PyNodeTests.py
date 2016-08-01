import unittest

from PyNode import *
from ActionNode import *
from AttributeNode import *

class CustomNode(PyNode):
    def __init__(self):
        super().__init__()

    @VirtualNode(name='@virtual_attribute')
    def virtual_attribute(self):
        if self.parent == None:
            return 1
        return self.parent.value + 1

    @VirtualNode
    def virtual(self):
        if self.parent == None:
            return "ra"
        return self.parent.value + "bar"

class PyNodeTests(unittest.TestCase):
    def setUp(self):
        self.node = CustomNode()

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

