import unittest
from contextshell.NodeTreeRoot import NodeTreeRoot
from contextshell.NodePath import NodePath
from tests.functional.ShellTestsBase import NodeTreeTestsBase
from tests.functional.TestExecutor import script_test


class ParserTypesTests(NodeTreeTestsBase):
    def install_custom_actions(self, tree: NodeTreeRoot):
        def type_of(target: NodePath, value_to_check):
            return type(value_to_check).__name__

        from contextshell.CallableAction import action_from_function
        tree.install_global_action(action_from_function(type_of))

    @script_test
    def test_int(self):
        """
        $ .: type.of 123
        int
        """

    @script_test
    def test_double_quoted_string(self):
        """
        $ .: type.of "rabarbar"
        str
        """

    @script_test
    def test_single_quoted_string(self):
        """
        $ .: type.of 'rabarbar'
        str
        """

    @script_test
    def test_float(self):
        """
        $ .: type.of 3.1415
        float
        """

    @unittest.skip("Not sure if required")
    @script_test
    def test_path(self):
        """
        $ .: type.of ra.bar.bar
        NodePath
        """
