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

if __name__ == '__main__':
    unittest.main()

