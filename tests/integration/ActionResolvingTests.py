from contextshell.NodePath import NodePath
from contextshell.Tree import Tree
from integration.ScriptTestBase import script_test
from integration.ShellTestsBase import ShellTestsBase


class ActionResolvingTests(ShellTestsBase):
    def install_actions(self, finder):
        def parent_action(tree: Tree, target: NodePath, action: NodePath):
            return "PARENT"

        finder.install_action(".", "parent_action", parent_action)

        def child_action(tree: Tree, target: NodePath, action: NodePath):
            return "CHILD"

        finder.install_action(".child", "child_action", child_action)

    @script_test
    def test_unknown_action(self):
        """
        > .: unknown_action
        NameError: Could not find action named 'unknown_action'
        """

    @script_test
    def test_parent_action_from_child(self):
        """
        > .child: parent_action
        PARENT
        """

    @script_test
    def test_child_action_from_child(self):
        """
        > .child: child_action
        CHILD
        """

    @script_test
    def test_parent_action_from_parent(self):
        """
        > .: parent_action
        PARENT
        """

    @script_test
    def test_child_action_from_parent(self):
        """
        > .: child_action
        NameError: Could not find action named 'child_action'
        """
