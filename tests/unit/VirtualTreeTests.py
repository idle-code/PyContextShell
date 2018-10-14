import unittest

from contextshell.backends.ActionExecutor import ActionExecutor, ActionArgsPack, OrderedDict, pack_argument_tree
from contextshell.NodePath import NodePath


def create_virtual_tree():
    from contextshell.VirtualTree import VirtualTree
    return VirtualTree()


def np(representation):
    return NodePath(representation)


class FakeActionExecutor(ActionExecutor):
    def __init__(self):
        self.execute_target = None
        self.execute_action = None
        self.execute_args = None
        self.execute_return = None

    def execute(self, target: NodePath, action: NodePath, args: ActionArgsPack = None):
        self.execute_target = target
        self.execute_action = action
        self.execute_args = args if args else OrderedDict()
        return self.execute_return


class MountTests(unittest.TestCase):
    def test_relative_target(self):
        vt = create_virtual_tree()
        tree_root = FakeActionExecutor()

        with self.assertRaises(ValueError):
            vt.mount(np("foo"), tree_root)

    def test_mount_visible_in_mapping(self):
        vt = create_virtual_tree()
        tree_root = FakeActionExecutor()

        vt.mount(np("."), tree_root)

        self.assertIn(np("."), vt.mounts)

    def test_mount_on_same_path(self):
        vt = create_virtual_tree()
        mount_path = np(".")
        vt.mount(mount_path, FakeActionExecutor())

        with self.assertRaises(KeyError):
            vt.mount(mount_path, FakeActionExecutor())

    def test_umount_removes_mapping(self):
        vt = create_virtual_tree()
        vt.mount(np("."), FakeActionExecutor())

        vt.umount(np("."))

        self.assertNotIn(np("."), vt.mounts)


class ExecuteTests(unittest.TestCase):
    def test_relative_target(self):
        vt = create_virtual_tree()
        vt.mount(np("."), FakeActionExecutor())

        with self.assertRaises(ValueError):
            vt.execute(np("foo"), np("action"))

    def test_no_matching_provider(self):
        vt = create_virtual_tree()
        vt.mount(np(".foo"), FakeActionExecutor())

        with self.assertRaises(RuntimeError):
            vt.execute(np(".bar"), np("action"))

    def test_target_remapping(self):
        """Target path is remapped to match provider's root"""
        vt = create_virtual_tree()
        tree_root = FakeActionExecutor()
        vt.mount(np(".foo"), tree_root)

        vt.execute(np(".foo.bar"), np("action"))

        self.assertEqual(np(".bar"), tree_root.execute_target)

    def test_action_forwarding(self):
        vt = create_virtual_tree()
        tree_root = FakeActionExecutor()
        vt.mount(np("."), tree_root)

        vt.execute(np("."), np("action"))

        self.assertEqual(np("action"), tree_root.execute_action)

    def test_args_forwarding(self):
        vt = create_virtual_tree()
        tree_root = FakeActionExecutor()
        vt.mount(np("."), tree_root)
        packed_args = pack_argument_tree('foo', 123)

        vt.execute(np("."), np("action"), packed_args)

        self.assertSequenceEqual(['foo', 123], tree_root.execute_args)

    def test_return_value_forwarding(self):
        vt = create_virtual_tree()
        tree_root = FakeActionExecutor()
        tree_root.execute_return = 'RETURN_VALUE'
        vt.mount(np("."), tree_root)

        action_result = vt.execute(np("."), np("action"))

        self.assertEqual('RETURN_VALUE', action_result)

    def test_most_specific_provider_is_matched(self):
        vt = create_virtual_tree()
        short_path_root = FakeActionExecutor()
        long_path_root = FakeActionExecutor()
        vt.mount(np(".foo"), short_path_root)
        vt.mount(np(".foo.bar"), long_path_root)

        vt.execute(np(".foo.bar.spam"), np("action"))

        self.assertEqual(np("action"), long_path_root.execute_action)


