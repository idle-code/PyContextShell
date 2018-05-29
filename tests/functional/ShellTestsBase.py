from contextshell.Shell import Shell
from contextshell.CommandInterpreter import CommandInterpreter
from contextshell.NodeTreeRoot import NodeTreeRoot
from contextshell.ActionFinder import ActionFinder
from functional.ScriptTestBase import ScriptTestBase
from abc import abstractmethod


class ShellTestsBase(ScriptTestBase):
    def create_shell(self):
        tree = NodeTreeRoot()
        action_finder = ActionFinder(tree)
        self.install_actions(action_finder)
        interpreter = CommandInterpreter(action_finder, tree)
        return Shell(interpreter)

    @abstractmethod
    def install_actions(self, action_finder: ActionFinder):
        raise NotImplementedError()