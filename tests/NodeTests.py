from Node import *

import unittest

DefaultAttributeCount = len(['@parent', '@name', '@path'])


class NodeBasicOperationsTests(unittest.TestCase):
    def setUp(self):
        self.intnode = Node(123)
        self.strnode = Node("spam")
        self.nonenode = Node()

    def test_get(self):
        self.assertEqual(123, self.intnode.value)
        self.assertEqual("spam", self.strnode.value)
        self.assertEqual(None, self.nonenode.value)

    def test_set(self):
        self.assertEqual(123, self.intnode.value)
        self.intnode.value = 321
        self.assertEqual(321, self.intnode.value)

    def test_typed_set(self):
        self.assertIs(int, type(self.intnode.value))
        with self.assertRaises(TypeError):
            self.intnode.value = "string value"

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

    # TODO: test call


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

    def test_path_indexing(self):
        leaf = Node("leaf")
        self.root.append_node('child.leaf', leaf)
        self.assertIn('leaf', self.root['child'].subnode_names)
        self.assertIs(leaf, self.root['child.leaf'])

    def test_path_numeric_indexing(self):
        r = Node()
        first = Node(1)
        second = Node(2)
        third = Node(3)
        r.append_node('first', first)
        r.append_node('second', second)
        r.append_node('third', third)

        self.assertIs(first, r[DefaultAttributeCount + 0])
        self.assertIs(second, r[DefaultAttributeCount + 1])
        self.assertIs(third, r[DefaultAttributeCount + 2])

        with self.assertRaises(TypeError):
            r.append_node(55, Node('fourth'))


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

    @unittest.skip("@parent virtual node is not supported now")
    def test_nested_parent_node(self):
        self.assertIs(self.child, self.child['@name']['@parent'])
        self.assertIs(self.child, self.child['@path']['@parent'])
        self.assertIs(self.root, self.child['@parent']['@parent'])

    def test_path_node(self):
        path_node = self.child['@path']
        self.assertIsInstance(path_node, Node)
        self.assertEqual(".child", path_node.value)

    def test_nested_path_node(self):
        self.assertEqual('.child.@name', self.child['@name']['@path'].value)
        self.assertEqual('.child.@path', self.child['@path']['@path'].value)
        #self.assertEqual('.child.@parent', self.child['@parent']['@path'].value)

    def test_name_node(self):
        name_node = self.child['@name']
        self.assertIsInstance(name_node, Node)
        self.assertEqual("child", name_node.value)

    def test_nested_name_node(self):
        self.assertEqual('@name', self.child['@name']['@name'].value)
        self.assertEqual('@path', self.child['@path']['@name'].value)
        #self.assertEqual('@parent', self.child['@parent']['@name'].value)

    def test_no_name(self):
        self.assertEqual(None, self.root['@name'].value)

    def test_index_node(self):
        index_node = self.child['@index']
        self.assertIs(self.child, self.root[index_node.value])

    def test_no_index(self):
        self.assertEqual(None, self.root['@index'].value)

if __name__ == '__main__':
    unittest.main()
