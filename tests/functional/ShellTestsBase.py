import unittest
from abc import ABC, abstractmethod
from contextshell.Shell import Shell
from contextshell.NodePath import NodePath
from contextshell.CommandInterpreter import CommandInterpreter
from contextshell.VirtualTree import VirtualTree
from contextshell.NodeTreeRoot import NodeTreeRoot
from contextshell.ActionFinder import ActionFinder


class VirtualTreeTestsBase(unittest.TestCase, ABC):
    def create_shell(self):
        self.virtual_tree = VirtualTree()
        self.register_roots(self.virtual_tree)

        interpreter = CommandInterpreter(self.virtual_tree)
        shell = Shell(interpreter)
        return shell

    @abstractmethod
    def register_roots(self, virtual_tree: VirtualTree):
        raise NotImplementedError()


class NodeTreeTestsBase(VirtualTreeTestsBase):
    def register_roots(self, virtual_tree: VirtualTree):
        tree_root = NodeTreeRoot()
        self.install_custom_actions(tree_root.action_finder)
        virtual_tree.mount(NodePath("."), tree_root)

    def install_custom_actions(self, action_finder: ActionFinder):
        pass
