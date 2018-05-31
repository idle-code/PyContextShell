import unittest
from contextshell.NodeTreeRoot import NodeTreeRoot
from contextshell.NodePath import NodePath
from functional.ShellTestsBase import NodeTreeTestsBase
from tests.functional.TestExecutor import script_test


class ParserTypesTests(NodeTreeTestsBase):
    def install_actions(self, finder):
        def type_of(tree: NodeTreeRoot, target: NodePath, action: NodePath, value):
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
