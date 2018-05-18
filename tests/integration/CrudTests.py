import unittest
from tests.integration.ScriptTestBase import ScriptTestBase, script_test


class CrudTests(ScriptTestBase):
    def create_shell(self):
        from contextshell.Shell import Shell
        from contextshell.CommandInterpreter import CommandInterpreter
        from contextshell.ActionFinder import ActionFinder
        from contextshell.Tree import Tree
        tree = Tree()
        action_finder = ActionFinder(tree)
        self._install_actions(action_finder)
        interpreter = CommandInterpreter(action_finder, tree)
        return Shell(interpreter)

    def _install_actions(self, finder):
        from contextshell.Tree import Tree
        from contextshell.NodePath import NodePath

        def exists(tree: Tree, target: NodePath, action: NodePath, name):
            return tree.exists(NodePath.join(target, name))

        finder.install_action(".", "exists", exists)

        def create(tree: Tree, target: NodePath, action: NodePath, name, value=None):
            tree.create(NodePath.join(target, name), value)

        finder.install_action(".", "create", create)

    @script_test
    def test_create(self):
        """
        > .: create foo
        > .: exists foo
        True
        """

    @script_test
    def test_exists_nonexistent(self):
        """
        > .: exists unknown
        False
        """

    @script_test
    def test_get(self):
        """
        > .: create foo 1
        > .foo: get
        1
        """
