import unittest
from abc import ABC, abstractmethod
from contextshell.Shell import Shell
from contextshell.NodePath import NodePath
from contextshell.CommandInterpreter import CommandInterpreter
from contextshell.VirtualTree import VirtualTree
from contextshell.NodeTreeRoot import NodeTreeRoot


class VirtualTreeTestsBase(unittest.TestCase, ABC):
    def create_shell(self):
        self.virtual_tree = VirtualTree()
        self.configure_virtual_tree(self.virtual_tree)

        interpreter = CommandInterpreter(self.virtual_tree)
        shell = Shell(interpreter)
        return shell

    @abstractmethod
    def configure_virtual_tree(self, virtual_tree: VirtualTree):
        raise NotImplementedError()


class NodeTreeTestsBase(VirtualTreeTestsBase):  # TODO: move to NodeTree tests
    def configure_virtual_tree(self, virtual_tree: VirtualTree):
        tree_root = NodeTreeRoot()
        self.configure_node_tree(tree_root)
        virtual_tree.mount(NodePath("."), tree_root)

    def configure_node_tree(self, tree: NodeTreeRoot):
        pass
