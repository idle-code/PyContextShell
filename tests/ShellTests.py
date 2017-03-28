import unittest
from Shell import *
from TreeRoot2 import TreeRoot


class ShellTests(unittest.TestCase):
    def setUp(self):
        self.root = TreeRoot()
        self.shell = Shell(self.root)

    def test_default_state(self):
        self.assertEqual(NodePath(absolute=True), self.shell.current_path)

    def test_create_empty(self):
        self.shell.execute("create foo")
        foo_value = self.shell.execute("foo: get")
        self.assertIsNone(foo_value)

    def test_create_string(self):
        self.shell.execute("create foo rabarbar")
        foo_value = self.shell.execute("foo: get")
        self.assertEqual('rabarbar', foo_value)

    def test_set_string(self):
        self.test_create_string()
        self.shell.execute("foo: set spam")
        foo_value = self.shell.execute("foo: get")
        self.assertEqual('spam', foo_value)

if __name__ == '__main__':
    unittest.main()
