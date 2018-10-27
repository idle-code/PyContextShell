import unittest


class ConstructorTests(unittest.TestCase):
    def create_tree(self, root_object):
        from contextshell.backends.python import PythonObjectTree
        return PythonObjectTree(root_object)

    def test_no_root_object(self):
        with self.assertRaises(ValueError):
            self.create_tree(None)
