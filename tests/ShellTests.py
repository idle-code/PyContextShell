import unittest
from Shell import *


class ShellTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.shell = Shell(self.root)

    def test_default_state(self):
        self.assertEqual(NodePath(absolute=True), self.shell.current_path)

    def test_create_empty(self):
        self.shell.execute("create foo")
        foo_value = self.shell.execute("foo: get")
        self.assertIsNone(foo_value)

    def test_create_int(self):
        self.shell.execute("create foo 123")
        foo_value = self.shell.execute("foo: get")
        self.assertEqual(123, foo_value)

    def test_set(self):
        self.test_create_int()
        self.shell.execute("foo: set 321")
        foo_value = self.shell.execute("foo: get")
        self.assertEqual(321, foo_value)

if __name__ == '__main__':
    unittest.main()
