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
        self.assertEqual(123, self.root.get('.bar'))

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

        self.assertEqual(123, self.root.get('.foo'))
        self.assertEqual(123, self.root.get('.foo_node'))
        self.assertEqual("text", self.root.get('.bar'))
        self.assertEqual("text", self.root.get('.bar_node'))

    def test_get(self):
        self.root.create(self.root, 'foo', 123)
        self.root.create(self.root, 'bar', "text")
        self.root.create(self.root, 'spam')

        self.assertEqual(123, self.root.get('.foo'))
        self.assertEqual("text", self.root.get('.bar'))
        self.assertEqual(None, self.root.get('.spam'))

        with self.assertRaises(NameError):
            self.root.get('.self.root')

    def test_set(self):
        self.test_get()

        self.root.set('.foo', 321)
        self.assertEqual(321, self.root.get('.foo'))

    def test_get_nested(self):
        self.root.create(self.root, 'foo')
        self.root.create(self.root['foo'], 'bar', 32)
        self.root.create(self.root['foo']['bar'], 'spam', "SPAM")

        self.assertEqual(32, self.root.get('.foo.bar'))
        self.assertEqual("SPAM", self.root.get('.foo.bar.spam'))

    def test_set_nested(self):
        self.test_get_nested()

        self.root.set('.foo.bar.spam', 321)
        self.assertEqual(321, self.root.get('.foo.bar.spam'))

    def test_name_attribute(self):
        self.root.create(self.root, 'foo', 123)

        self.assertEqual('foo', self.root.get('.foo.@name'))

    def test_exists(self):
        self.test_get()

        self.assertTrue(self.root.exists('.foo'))
        self.assertFalse(self.root.exists('.invalid_key'))

    def test_delete(self):
        self.test_get()

        self.assertTrue(self.root.exists('.foo'))
        self.root.delete('foo')
        self.assertFalse(self.root.exists('.foo'))

if __name__ == '__main__':
    unittest.main()

