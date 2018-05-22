import unittest
from contextshell.Tree import Tree
from contextshell.NodePath import NodePath
from integration.ShellTestsBase import ShellTestsBase
from tests.integration.ScriptTestBase import script_test


class ParserTypesTests(ShellTestsBase):
    def install_actions(self, finder):
        def type_of(tree: Tree, target: NodePath, action: NodePath, value):
            return type(value).__name__

        finder.install_action(".", "type.of", type_of)

    @script_test
    def test_int(self):
        """
        > .: type.of 123
        int
        """

    @script_test
    def test_double_quoted_string(self):
        """
        > .: type.of "rabarbar"
        str
        """

    @script_test
    def test_single_quoted_string(self):
        """
        > .: type.of 'rabarbar'
        str
        """

    @script_test
    def test_float(self):
        """
        > .: type.of 3.1415
        float
        """

    @unittest.skip("Not sure if required")
    @script_test
    def test_path(self):
        """
        > .: type.of ra.bar.bar
        NodePath
        """
