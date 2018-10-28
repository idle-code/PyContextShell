from contextshell.backends.node import NodeTreeRoot
from contextshell.path import NodePath
from tests.functional.bases import NodeTreeTestsBase
from tests.functional.TestExecutor import script_test


class ActionResolvingTests(NodeTreeTestsBase):
    def configure_node_tree(self, tree: NodeTreeRoot):
        from contextshell.action import action_from_function

        def parent(target: NodePath):
            return "PARENT"

        tree.install_global_action(action_from_function(parent))

        def child(target: NodePath):
            return "CHILD"

        tree.install_action(NodePath(".child"), action_from_function(child))

        def multi_part(target: NodePath):
            pass

        tree.install_global_action(action_from_function(multi_part))

    @script_test
    def test_unknown_action(self):
        """
        $ .: unknown
        NameError: Could not find action named 'unknown'
        """

    @script_test
    def test_parent_action_from_child(self):
        """
        $ .child: parent
        PARENT
        """

    @script_test
    def test_child_action_from_child(self):
        """
        $ .child: child
        CHILD
        """

    @script_test
    def test_parent_action_from_parent(self):
        """
        $ .: parent
        PARENT
        """

    @script_test
    def test_child_action_from_parent(self):
        """
        $ .: child
        NameError: Could not find action named 'child'
        """

    @script_test
    def test_non_action_invoke(self):
        """
        $ .: multi
        NameError: Could not find action named 'multi'
        """
