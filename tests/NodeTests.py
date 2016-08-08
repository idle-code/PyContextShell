from Node import *

import unittest

DefaultAttributeCount = 2

class NodeBasicOperationsTests(unittest.TestCase):
    def test_constructor(self):
        intnode = Node(123)
        strnode = Node("spam")
        nonenode = Node()

    def test_get(self):
        intnode = Node(123)
        self.assertEqual(123, intnode.value)

        strnode = Node("spam")
        self.assertEqual("spam", strnode.value)

        nonenode = Node()
        self.assertEqual(None, nonenode.value)

    def test_set(self):
        intnode = Node(123)
        self.assertEqual(123, intnode.value)
        intnode.value = 321
        self.assertEqual(321, intnode.value)

    def test_typed_set(self):
        intnode = Node(123)
        self.assertEqual(123, intnode.value)

        with self.assertRaises(TypeError):
            intnode.value = "other type"

    def test_empty_list(self):
        empty_node = Node()
        self.assertEqual(DefaultAttributeCount, len(empty_node.subnodes))

    def test_list(self):
        node = Node()
        node.append_node('a', Node(1))
        node.append_node('b', Node(2))
        node.append_node('c', Node(3))

        self.assertEqual(DefaultAttributeCount + 3, len(node.subnodes))
        node_values = list(map(lambda n: n.value, node.subnodes))
        self.assertTrue(1 in node_values)
        self.assertTrue(2 in node_values)
        self.assertTrue(3 in node_values)

        self.assertEqual(DefaultAttributeCount + 3, len(node.subnode_names))
        self.assertTrue('a' in node.subnode_names)
        self.assertTrue('b' in node.subnode_names)
        self.assertTrue('c' in node.subnode_names)

    #TODO: test call

class NodeTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.child = Node(999)
        self.root.append_node('child', self.child)

    def test_replace_node(self):
        self.child.value = 1
        self.assertEqual(1, self.root['child'].value)
        self.assertIs(self.root, self.root['child'].parent)

        new_node = Node(2)
        self.root.replace_node('child', new_node)
        self.assertEqual(2, self.root['child'].value)
        self.assertIs(self.root, self.root['child'].parent)
        self.assertIs(None, self.child.parent)

    def test_parent(self):
        self.assertIs(None, self.root.parent)
        self.assertIs(self.root, self.root['child'].parent)

    def test_path(self):
        self.assertEqual(".child", self.child.path)

    def test_name(self):
        self.assertEqual("child", self.child.name)

class NodeVirtualNodesTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.child = Node()
        self.root.append_node('child', self.child)

    @unittest.skip("@parent virtual node is not supported now")
    def test_parent_node(self):
        parent_node = self.child['@parent']
        self.assertIsInstance(parent_node, Node)
        self.assertIs(self.root, parent_node)

    def test_path_node(self):
        path_node = self.child['@path']
        self.assertIsInstance(path_node, Node)
        self.assertEqual(".child", path_node.value)

    def test_name_node(self):
        name_node = self.child['@name']
        self.assertIsInstance(name_node, Node)
        self.assertEqual("child", name_node.value)

    def test_nested_name_node(self):
        self.assertEqual('@name', self.child['@name']['@name'].value)
        self.assertEqual('@path', self.child['@path']['@name'].value)
        #self.assertEqual('@parent', self.child['@parent']['@name'].value)

    def test_nested_path_node(self):
        self.assertEqual('.child.@name', self.child['@name']['@path'].value)
        self.assertEqual('.child.@path', self.child['@path']['@path'].value)
        #self.assertEqual('.child.@parent', self.child['@parent']['@path'].value)

    @unittest.skip("@parent virtual node is not supported now")
    def test_nested_parent_node(self):
        self.assertIs(self.child, self.child['@name']['@parent'])
        self.assertIs(self.child, self.child['@path']['@parent'])
        self.assertIs(self.root, self.child['@parent']['@parent'])

if __name__ == '__main__':
    unittest.main()

