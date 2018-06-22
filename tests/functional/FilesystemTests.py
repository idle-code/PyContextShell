import unittest
from contextshell.VirtualTree import VirtualTree
from contextshell.NodeTreeRoot import NodeTreeRoot
from contextshell.NodePath import NodePath
from tests.functional.ShellTestsBase import VirtualTreeTestsBase
from tests.functional.TestExecutor import script_test


class FilesystemTestsBase(VirtualTreeTestsBase):
    def configure_virtual_tree(self, virtual_tree: VirtualTree):
        # TODO: Create FilesystemTreeNode
        pass

    def configure_node_tree(self, tree: NodeTreeRoot):
        def attach_filesystem(target: NodePath, mount_point: NodePath):
            tree.create(NodePath(mount_point))

        def detach(target: NodePath):
            tree.remove(target)

        from contextshell.CallableAction import action_from_function
        tree.install_global_action(action_from_function(attach_filesystem))
        tree.install_global_action(action_from_function(detach))


@unittest.skip("Re-enable when filesystem module can be installed")
class AttachTests(VirtualTreeTestsBase):
    def configure_virtual_tree(self, virtual_tree: VirtualTree):
        # TODO: install filesystem module/actions fot attaching
        # Note: VirtualTreeRoot *CAN* append data to the invoked commands
        # i.e. it can add attach.* commands to output of 'list.actions' (for completion)
        # TODO: find a (easy) way to support custom actions in VirtualTreeRoot
        pass

    @script_test
    def test_attach(self):
        """
        $ .: attach.filesystem .fs
        $ .: contains fs
        True
        """

    @script_test
    def test_detach(self):
        """
        $ .: attach.filesystem .fs
        $ .fs: detach
        $ .: contains fs
        False
        """


@unittest.skip("Re-enable when filesystem root is available")
class IsTests(FilesystemTestsBase):
    @script_test
    def test_contains_directory(self):
        """
        $ .: attach.filesystem .fs
        $ .fs: contains test_directory
        True
        """

    @script_test
    def test_contains_file(self):
        """
        $ .: attach.filesystem .fs
        $ .fs: contains test_file
        True
        """

    @script_test
    def test_is_directory(self):
        """
        $ .: attach.filesystem .fs
        $ .fs.test_directory: is.directory
        True
        $ .fs.test_directory: is.file
        False
        """

    @script_test
    def test_is_file(self):
        """
        $ .: attach.filesystem .fs
        $ .fs.test_file: is.directory
        False
        $ .fs.test_file: is.file
        True
        """
