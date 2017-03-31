from NodePath import *
from Node2 import *

import unittest


class NodePathTests(unittest.TestCase):
    def test_empty(self):
        empty = NodePath()
        self.assertEqual(0, len(empty))
        self.assertFalse(empty.is_absolute)

    def test_constructor(self):
        l = NodePath(['a', 'b', 'c'])
        self.assertEqual(3, len(l))
        self.assertFalse(l.is_absolute)
        self.assertEqual('a.b.c', str(l))

    def test_parse(self):
        p = NodePath('a.b.c')
        self.assertEqual(3, len(p))
        self.assertFalse(p.is_absolute)
        self.assertEqual('a.b.c', str(p))

        pa = NodePath('.a.b.c')
        self.assertEqual(3, len(pa))
        self.assertTrue(pa.is_absolute)
        self.assertEqual('.a.b.c', str(pa))

    def test_basename(self):
        abc = NodePath('a.b.c')
        self.assertEqual('c', abc.base_name)

        base_path = abc.base_path
        self.assertEqual(2, len(base_path))
        self.assertFalse(base_path.is_absolute)
        self.assertEqual('a.b', str(base_path))
        self.assertEqual('b', base_path.base_name)

    def test_index(self):
        ab2c = NodePath(['a', 'b', 2, 'c'])

        self.assertEqual(4, len(ab2c))
        self.assertEqual('a.b.2.c', str(ab2c))

    def test_index_parse(self):
        ab2c = NodePath('.a.b.2.c')

        self.assertEqual(4, len(ab2c))
        self.assertEqual('.a.b.2.c', str(ab2c))
        self.assertIsInstance(ab2c[2], int)

    def test_cast(self):
        none = NodePath.cast(None)
        self.assertEqual(0, len(none))
        self.assertFalse(none.is_absolute)

        name = NodePath.cast('foo')
        self.assertEqual(1, len(name))
        self.assertFalse(name.is_absolute)
        self.assertIsInstance(name[0], str)

        path = NodePath.cast('.foo.bar.baz')
        self.assertEqual(3, len(path))
        self.assertTrue(path.is_absolute)

        path = NodePath.cast(['foo', 'bar', 'baz'])
        self.assertEqual(3, len(path))
        self.assertFalse(path.is_absolute)

    def test_node_cast_mutability(self):
        foobar = NodePath(['foo', 'bar'])
        casted = NodePath.cast(foobar)
        foobar.append('baz')

        self.assertListEqual(['foo', 'bar', 'baz'], foobar)
        self.assertListEqual(['foo', 'bar'], casted)

    def test_cast_index(self):
        number = NodePath.cast(13)
        self.assertEqual(1, len(number))
        self.assertFalse(number.is_absolute)
        self.assertIsInstance(number[0], int)
        self.assertEqual(13, number[0])

        strnumber = NodePath.cast('42')
        self.assertEqual(1, len(strnumber))
        self.assertFalse(strnumber.is_absolute)
        self.assertEqual(42, strnumber[0])

    def test_join(self):
        foobar = NodePath('.foo.bar')
        spam = NodePath('.spam')

        foobarspam = NodePath.join(foobar, spam)
        self.assertEqual('.foo.bar.spam', str(foobarspam))
        self.assertEqual(3, len(foobarspam))

    def test_join_mutability(self):
        foobar = NodePath('.foo.bar')
        spam = NodePath('.spam')

        foobarspam = NodePath.join(foobar, spam)
        self.assertEqual('.foo.bar.spam', str(foobarspam))
        self.assertEqual('.foo.bar', str(foobar))
        self.assertEqual('.spam', str(spam))

    def test_join_raw(self):
        rabarbar = NodePath.join('ra', 'bar', 'bar')
        self.assertEqual('ra.bar.bar', str(rabarbar))
        self.assertEqual(3, len(rabarbar))


class HelperMethodsTests(unittest.TestCase):
    def setUp(self):
        self.root = Node('root')
        self.foo = Node('foo')
        self.root.append('foo', self.foo)
        self.bar = Node('bar')
        self.foo.append('bar', self.bar)

    def test_create_path_relative(self):
        spam_path = NodePath('spam.baz')
        baz_node = NodePath.create_path(self.foo, spam_path)
        self.assertIsNotNone(baz_node)
        spam_node = self.root['foo'].get_node('spam')
        self.assertIsNotNone(spam_node)
        self.assertIsNone(spam_node.get())
        self.assertIsNotNone(spam_node.get_node('baz'))

    def test_create_path_partially_existing(self):
        spam_path = NodePath('foo.spam')
        spam_node = NodePath.create_path(self.root, spam_path)
        self.assertIsNotNone(spam_node)
        self.assertIsNotNone(self.root['foo'].get_node('spam'))

    def test_create_path_existing(self):
        bar_path = NodePath('foo.bar')
        bar_node = NodePath.create_path(self.root, bar_path)
        self.assertIs(self.bar, bar_node)

    def test_create_path_absolute(self):
        # TODO: check if this is correct behaviour
        spam_path = NodePath('.foo.spam')
        with self.assertRaises(NotImplementedError):
            NodePath.create_path(self.bar, spam_path)

if __name__ == '__main__':
    unittest.main()
