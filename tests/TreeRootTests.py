import unittest

from TreeRoot import *


class TreeRootTests(unittest.TestCase):
    def setUp(self):
        self.root = TreeRoot()

    @unittest.skip("FIXME")
    def test_create_call(self):
        self.root.call('.', 'create', 'foo')
        self.assertTrue('foo' in self.root)

        self.root.call('.', 'create', 'bar', 123)
        self.assertTrue(self.root.contains('bar'))
        self.assertEqual(123, self.root.get(self.root['bar']))

    def test_create_existing(self):
        self.root.create(self.root, 'foo', 123)
        with self.assertRaises(NameError):
            self.root.create(self.root, 'foo')

    @unittest.skip
    def test_create(self):
        self.root.create(self.root, 'foo', 123)
        self.assertTrue(self.root.contains('foo'))
        self.assertEqual(123, self.root.get(self.root['.foo']))

        self.root.create(self.root, 'foo_node', Node(123))
        self.assertTrue(self.root.contains('foo_node'))
        self.assertEqual(123, self.root.get(self.root['.foo_node']))

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

    @unittest.skip
    def test_name_attribute(self):
        self.root.create(self.root, 'foo', 123)

        self.assertEqual('foo', self.root.get(self.root['foo']['@name']))

    @unittest.skip
    def test_list(self):
        self.test_get()

        root_subnodes = self.root.list(self.root)
        subnode_names = list(map(lambda n: n['@name'].value, root_subnodes))
        self.assertListEqual(['foo', 'bar', 'spam'], subnode_names)

    @unittest.skip
    def test_exists(self):
        self.test_get()

        self.assertTrue(self.root.contains(self.root, 'foo'))
        self.assertFalse(self.root.contains(self.root, 'invalid_key'))

    @unittest.skip
    def test_delete(self):
        self.test_get()

        self.assertTrue(self.root.contains(self.root, 'foo'))
        self.root.delete(self.root, 'foo')
        self.assertFalse(self.root.contains(self.root, 'foo'))

    @unittest.skip
    def test_delete_nonexistent(self):
        self.assertFalse(self.root.contains(self.root, 'foo'))
        with self.assertRaises(NameError):
            self.root.delete(self.root, 'foo')


class ActionTests(unittest.TestCase):
    def setUp(self):
        self.root = TreeRoot()
        self.root.append('foo', Node('foo'))
        self.root['foo'].append('bar', Node('bar'))
        self.root.append('spam', Node(123))


class ListActionTests(ActionTests):
    @unittest.skip
    def test_list_nodes(self):
        nodes = self.root.list(self.root)
        self.assertEqual(2, len(nodes))
        self.assertListEqual(nodes, [self.root['foo'], self.root['spam']])

if __name__ == '__main__':
    unittest.main()

