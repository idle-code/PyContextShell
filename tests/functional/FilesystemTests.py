import unittest
from contextshell.NodeTreeRoot import NodeTreeRoot
from contextshell.NodePath import NodePath
from tests.functional.ShellTestsBase import NodeTreeTestsBase
from tests.functional.TestExecutor import script_test


#@unittest.skip("TODO after virtual tree interface")
class FilesystemTestsBase(NodeTreeTestsBase):
    def configure_tree(self, tree: NodeTreeRoot):
        def attach_filesystem(target: NodePath, mount_point: NodePath):
            tree.create(NodePath(mount_point))
            return None

        from contextshell.CallableAction import action_from_function
        tree.install_global_action(action_from_function(attach_filesystem))

    @script_test
    def test_mount(self):
        """
        $ .: attach.filesystem .fs
        $ .: contains .fs
        True
        """
