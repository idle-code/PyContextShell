import unittest

from Tree import *

class TreeTests(unittest.TestCase):
    def setUp(self):
        self.root = Tree()

    def test_create(self):
        self.root.create('foo', 123)
        self.root.create('bar', "text")
        self.root.create('spam')

        with self.assertRaises(NameError):
            self.root.create('foo')

    def test_get(self):
        self.root.create('foo', 123)
        self.root.create('bar', "text")
        self.root.create('spam')

        self.assertEqual(123, self.root.get('foo'))
        self.assertEqual("text", self.root.get('bar'))
        self.assertEqual(None, self.root.get('spam'))

        with self.assertRaises(NameError):
            self.root.get('rabarbar')

    def test_set(self):
        self.test_get()

        self.root.set('foo', 321)
        self.assertEqual(321, self.root.get('foo'))

    def test_get_nested(self):
        self.root.create('foo')
        self.root.create('foo.bar', 32)
        self.root.create('foo.bar.spam', "SPAM")

        self.assertEqual(32, self.root.get('foo.bar'))
        self.assertEqual("SPAM", self.root.get('foo.bar.spam'))

    def test_set_nested(self):
        self.test_get_nested()

        self.root.set('foo.bar.spam', 321)
        self.assertEqual(321, self.root.get('foo.bar.spam'))

    def test_name_attribute(self):
        self.root.create('foo', 123)

        self.assertEqual('foo', self.root.get('foo.@name'))

    def test_exists(self):
        self.test_get()

        self.assertTrue(self.root.exists('foo'))
        self.assertFalse(self.root.exists('invalid_key'))

    def test_delete(self):
        self.test_get()

        self.assertTrue(self.root.exists('foo'))
        self.root.delete('foo')
        self.assertFalse(self.root.exists('foo'))


if __name__ == '__main__':
    unittest.main()

