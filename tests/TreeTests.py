import unittest
from contextshell.NodePath import NodePath as np


def create_tree(*args, **kwargs):
    from contextshell.Tree import Tree
    if 'root_node' in kwargs:
        root_node = kwargs['root_node']
    else:
        from contextshell.Node import Node
        root_node = Node()

    return Tree(root_node)


class TreeTests(unittest.TestCase):
    def test_constructor_when_no_root_node_provided_throws(self):
        with self.assertRaises(ValueError):
            create_tree(root_node=None)


class CreateTests(unittest.TestCase):
    def test_create_with_relative_path_throws(self):
        tree = create_tree()
        relative_path = np('relative')

        with self.assertRaises(ValueError):
            tree.create(relative_path)

    def test_create_default(self):
        tree = create_tree()
        foo_path = np('.foo')

        tree.create(foo_path)
        foo_exists = tree.exists(foo_path)

        self.assertTrue(foo_exists)

    def test_create_with_initial_value(self):
        tree = create_tree()
        foo_path = np('.foo')

        tree.create(foo_path, 3)
        foo_value = tree.get(foo_path)

        self.assertEqual(3, foo_value)

    def test_create_existing_throws(self):
        tree = create_tree()
        existing_path = np('.existing')
        tree.create(existing_path)

        # TODO: check if this is right exception type
        with self.assertRaises(NameError):
            tree.create(existing_path)

    # FIXME: am I testing Tree class or Node here?
