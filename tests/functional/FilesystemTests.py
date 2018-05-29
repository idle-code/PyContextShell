import unittest
from contextshell.NodeTreeRoot import NodeTreeRoot
from contextshell.NodePath import NodePath
from functional.ShellTestsBase import ShellTestsBase
from tests.functional.ScriptTestBase import script_test


@unittest.skip("TODO after virtual tree interface")
class CrudTestsBase(ShellTestsBase):
    def install_actions(self, finder):
        # TODO: install filesystem module
        pass

    @script_test
    def test_mount(self):
        """
        > .: filesystem.mount.as .fs
        > .fs: exists
        True
        """
