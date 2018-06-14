import unittest
from contextshell.NodeTreeRoot import NodeTreeRoot
from contextshell.NodePath import NodePath
from tests.functional.ShellTestsBase import NodeTreeTestsBase
from tests.functional.TestExecutor import script_test


@unittest.skip("TODO after virtual tree interface")
class FilesystemTestsBase(NodeTreeTestsBase):
    def install_custom_actions(self, finder):
        # TODO: install filesystem module
        pass

    @script_test
    def test_mount(self):
        """
        $ .: filesystem.mount.as .fs
        $ .fs: exists
        True
        """
