import unittest
from typing import Dict, Union, Any
from tests.unit.Fakes import FakeAction
from contextshell.NodePath import NodePath as np
from contextshell.NodePath import NodePath
from contextshell.TreeRoot import TreeRoot


def create_tree(*args, **kwargs):
    from contextshell.NodeTreeRoot import NodeTreeRoot
    return NodeTreeRoot(*args)


class ConstructionTests(unittest.TestCase):
    def test_root_have_no_value(self):
        # CHECK: I am unsure if this tests any behaviour
        tree = create_tree()

        root_value = tree.root.get()

        self.assertIsNone(root_value)


class CreatePathTests(unittest.TestCase):
    def test_relative_path_throws(self):
        tree = create_tree()
        relative_path = np("foo")

        with self.assertRaises(ValueError):
            tree._create_path(relative_path)

    def test_create_multiple_elements(self):
        tree = create_tree()
        long_path = np(".foo.bar")

        tree._create_path(long_path)

        self.assertTrue(tree.exists(np(".foo")))
        self.assertTrue(tree.exists(long_path))

    def test_create_already_existing(self):
        tree = create_tree()
        existing_path = np(".foo")
        created_node = tree._create_path(existing_path)

        resolved_node = tree._create_path(existing_path)

        self.assertIs(created_node, resolved_node)


class ResolveOptionalTests(unittest.TestCase):
    def test_resolve_optional_relative_path_throws(self):
        tree = create_tree()
        relative_path = np("foo")

        with self.assertRaises(ValueError):
            tree._resolve_optional_path(relative_path)

    def test_resolve_optional_existing(self):
        tree = create_tree()
        existing_path = np(".foo.bar")
        tree.create(existing_path, 'BAR')

        resolved_node = tree._resolve_optional_path(existing_path)

        self.assertIs('BAR', resolved_node.get())

    def test_resolve_optional_nonexistent(self):
        tree = create_tree()
        nonexistent_path = np(".foo.bar")

        resolved_node = tree._resolve_optional_path(nonexistent_path)

        self.assertIsNone(resolved_node)

    def test_resolve_optional_partially_existing(self):
        tree = create_tree()
        tree.create(np('.foo'))
        nonexistent_path = np(".foo.bar")

        resolved_node = tree._resolve_optional_path(nonexistent_path)

        self.assertIsNone(resolved_node)


class ResolveTests(unittest.TestCase):
    def test_resolve_relative_path_throws(self):
        tree = create_tree()
        relative_path = np("foo")

        with self.assertRaises(ValueError):
            tree._resolve_path(relative_path)

    def test_resolve_existing(self):
        tree = create_tree()
        existing_path = np(".foo.bar")
        tree.create(existing_path, 'BAR')

        resolved_node = tree._resolve_path(existing_path)

        self.assertIs('BAR', resolved_node.get())

    def test_resolve_nonexistent(self):
        tree = create_tree()
        nonexistent_path = np(".foo.bar")

        with self.assertRaises(NameError):
            tree._resolve_path(nonexistent_path)


class CreateTests(unittest.TestCase):
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

    def test_create_multilevel_default(self):
        tree = create_tree()
        long_path = np(".foo.bar.spam")

        tree.create(long_path)

        self.assertTrue(tree.exists(long_path))

    def test_create_multilevel_with_initial_value(self):
        tree = create_tree()
        long_path = np(".foo.bar.spam")

        tree.create(long_path, 2)

        final_value = tree.get(long_path)
        self.assertEqual(2, final_value)


class ExistsTests(unittest.TestCase):
    def test_exists_nonexistent(self):
        tree = create_tree()
        nonexistent_path = np('.nonexistent')

        exists = tree.exists(nonexistent_path)

        self.assertFalse(exists)

    def test_exists_existing(self):
        tree = create_tree()
        existing_path = np('.path')
        tree.create(existing_path)

        exists = tree.exists(existing_path)

        self.assertTrue(exists)


class GetTests(unittest.TestCase):
    def test_return_value(self):
        tree = create_tree()
        existing_path = np('.path')
        tree.create(existing_path, 3)

        get_value = tree.get(existing_path)

        self.assertEqual(3, get_value)


class SetTests(unittest.TestCase):
    def test_update_value(self):
        tree = create_tree()
        existing_path = np('.path')
        tree.create(existing_path, 1)

        tree.set(existing_path, 2)

        updated_value = tree.get(existing_path)
        self.assertEqual(2, updated_value)


class ListTests(unittest.TestCase):
    def test_empty(self):
        tree = create_tree()
        tree.create(np('.empty'))

        empty_list = tree.list(np('.empty'))

        self.assertSequenceEqual([], empty_list)

    def test_single(self):
        tree = create_tree()
        existing_path = np('.path')
        tree.create(existing_path)

        root_list = tree.list(np('.'))

        self.assertIn(np("path"), root_list)


class RemoveTests(unittest.TestCase):
    def test_remove_existing(self):
        tree = create_tree()
        existing_path = np('.foo')
        tree.create(existing_path, 3)

        tree.remove(existing_path)

        self.assertFalse(tree.exists(existing_path))

    def test_remove_root(self):
        tree = create_tree()

        with self.assertRaises(ValueError):
            tree.remove(np('.'))


class IsActionTests(unittest.TestCase):
    def test_installed_action(self):
        tree = create_tree()
        tree.install_global_action(FakeAction('test'))
        test_action_path = np('.@actions.test')  # CHECK: get path from installation? resolve.action?

        test_is_action = tree.is_action(test_action_path)

        self.assertTrue(test_is_action)

    def test_is_not_action(self):
        tree = create_tree()
        foo_path = np(".foo")
        tree.create(foo_path)

        foo_is_action = tree.is_action(foo_path)

        self.assertFalse(foo_is_action)


class ListActions(unittest.TestCase):
    default_actions = [
        'create',
        'exists',
        'get',
        'list',
        'remove',
        'set',
    ]

    def test_default_actions(self):
        tree = create_tree()

        root_actions = tree.list_actions(np('.'))

        self.assertSequenceEqual(ListActions.default_actions, root_actions)

    def test_node_specific_actions(self):
        tree = create_tree()
        child_path = np('.child')
        tree.create(child_path)
        tree.install_action(child_path, FakeAction('test'))

        child_actions = tree.list_actions(child_path)

        self.assertSequenceEqual(['test'] + ListActions.default_actions, child_actions)


class FindActionTests(unittest.TestCase):
    def test_find_nonexistent_target(self):
        tree = create_tree()
        global_action = FakeAction(np('action'))
        tree.install_global_action(global_action)

        found_action = tree.find_action(np('.nonexistent'), np('action'))

        self.assertIs(global_action, found_action)

    def test_find_nonexistent_action(self):
        tree = create_tree()

        found_action = tree.find_action(np('.'), np('action'))

        self.assertIsNone(found_action)

    def test_find_invalid_action(self):
        tree = create_tree()
        tree.create(np('.@actions.action'), 123)

        found_action = tree.find_action(np('.'), np('action'))

        self.assertIsNone(found_action)

    def test_resolve_order_target_before_type(self):
        tree = create_tree()
        action_name = np('action')
        type_action = FakeAction(action_name)
        target_action = FakeAction(action_name)
        tree.create(np('.target'))
        tree.install_action(np('.target.@type'), type_action)
        tree.install_action(np('.target'), target_action)

        found_action = tree.find_action(np('.target'), action_name)

        self.assertIs(target_action, found_action)

    def test_resolve_order_type_before_global(self):
        tree = create_tree()
        tree.create(np('.target.@type'))
        action_name = np('action')
        global_action = FakeAction(action_name)
        type_action = FakeAction(action_name)
        tree.install_global_action(global_action)
        tree.install_action(np('.target.@type'), type_action)

        found_action = tree.find_action(np('.target'), action_name)

        self.assertIs(type_action, found_action)


# from contextshell.NodeTreeRoot import NodeTreeRoot
# class TestedNodeTreeRoot(NodeTreeRoot):
#     def no_args_action(self):
#         return 'NO_ARGS'
#
#
# class ArgumentUnpackerTests(unittest.TestCase):
#     def test_unpack_none(self):
#         tree = TestedNodeTreeRoot()
#
#         wrapped_action = tree.arg_unpacker(TestedNodeTreeRoot.no_args_action)
#         return_value = wrapped_action(tree)
#
#         self.assertEqual('NO_ARGS', return_value)
#
#     def test_unpack_none(self):
#         tree = TestedNodeTreeRoot()
#
#         wrapped_action = tree.arg_unpacker(TestedNodeTreeRoot.no_args_action)
#         return_value = wrapped_action(tree)
#
#         self.assertEqual('NO_ARGS', return_value)
