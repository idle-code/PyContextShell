import unittest
from tests.integration.ScriptTestBase import ScriptTestBase, script_test


class CrudTests(ScriptTestBase):
    def create_shell(self):
        from contextshell.Shell import Shell
        from contextshell.CommandInterpreter import CommandInterpreter
        from contextshell.ActionFinder import ActionFinder
        from contextshell.Tree import Tree
        #from Fakes import FakeTree
        #tree = FakeTree()
        tree = Tree()
        self._install_actions(tree)
        action_finder = ActionFinder(tree)
        interpreter = CommandInterpreter(action_finder, tree)
        return Shell(interpreter)

    def _install_actions(self, tree):
        pass  # TODO implement or use DefaultTree (or something...)

    @unittest.skip("TODO: run when actions are installed")
    @script_test
    def test_create(self):
        """
        > .: create foo
        > .: exists foo
        True
        """

    @unittest.skip("TODO: run when actions are installed")
    @script_test
    def test_exists_nonexistent(self):
        """
        > .: exists unknown
        False
        """

    @unittest.skip("TODO: run when Tree class is ready")
    @script_test
    def test_get(self):
        """
        > .: create foo 1
        > .foo: get
        1
        """
