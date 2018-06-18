from contextshell.NodeTreeRoot import NodeTreeRoot
from tests.functional.ShellTestsBase import NodeTreeTestsBase
from tests.functional.TestExecutor import script_test
import unittest


class NodeType:
    pass


class CustomType(NodeType):
    pass


class CustomTypeTests(NodeTreeTestsBase):
    def configure_tree(self, tree: NodeTreeRoot):
        tree.install_global_type(CustomType())

    @unittest.skip("Type system not ready yet")
    @script_test
    def test_created_custom_exists(self):
        """
        $ .: create.custom c
        $ .: exists c
        """
