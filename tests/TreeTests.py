import unittest

from Tree import *

class TreeTests(unittest.TestCase):
    def setUp(self):
        self.root = Tree()

    def test_create_command(self):
        self.root.call('.', 'create', 'foo')
        self.assertTrue('foo' in self.root)

        self.root.call('.', 'create', 'bar', 123)
        self.assertTrue('bar' in self.root)
        self.assertEqual(123, self.root.get(self.root['bar']))

    def test_create(self):
        self.root.create(self.root, 'foo', 123)
        self.root.create(self.root, 'foo_node', Node(123))
        self.root.create(self.root, 'bar', "text")
        self.root.create(self.root, 'bar_node', Node("text"))
        self.root.create(self.root, 'spam')

        with self.assertRaises(NameError):
            self.root.create(self.root, 'foo')
        return
        with self.assertRaises(NameError):
            self.root.create(self.root, 'foo_node')
        with self.assertRaises(NameError):
            self.root.create(self.root, 'spam')

        self.assertTrue('bar' in self.root)
        self.assertTrue('bar_node' in self.root)

        self.assertEqual(123, self.root.get(self.root, '.foo'))
        self.assertEqual(123, self.root.get('.foo_node'))
        self.assertEqual("text", self.root.get('.bar'))
        self.assertEqual("text", self.root.get('.bar_node'))

    def test_get(self):
        self.root.create(self.root, 'foo', 123)
        self.root.create(self.root, 'bar', "text")
        self.root.create(self.root, 'spam')

        self.assertEqual(123, self.root.get(self.root['foo']))
        self.assertEqual("text", self.root.get(self.root['bar']))
        self.assertEqual(None, self.root.get(self.root['spam']))

    def test_set(self):
        self.test_get()

        self.root.set(self.root['foo'], 321)
        self.assertEqual(321, self.root.get(self.root['foo']))

    def test_name_attribute(self):
        self.root.create(self.root, 'foo', 123)

        self.assertEqual('foo', self.root.get(self.root['foo']['@name']))

    def test_list(self):
        self.test_get()

        root_subnodes = self.root.list(self.root)
        subnode_names = list(map(lambda n: n['@name'].value, root_subnodes))
        self.assertListEqual(['foo', 'bar', 'spam'], subnode_names)

    def test_exists(self):
        self.test_get()

        self.assertTrue(self.root.exists(self.root, 'foo'))
        self.assertFalse(self.root.exists(self.root, 'invalid_key'))

    def test_delete(self):
        self.test_get()

        self.assertTrue(self.root.exists(self.root, 'foo'))
        self.root.delete(self.root, 'foo')
        self.assertFalse(self.root.exists(self.root, 'foo'))

    def test_delete_nonexisting(self):
        self.assertFalse(self.root.exists(self.root, 'foo'))
        with self.assertRaises(NameError):
            self.root.delete(self.root, 'foo')

if __name__ == '__main__':
    unittest.main()

