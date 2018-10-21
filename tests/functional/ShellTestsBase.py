import unittest
from abc import ABC, abstractmethod

from contextshell.action import ActionExecutor, Executor
from contextshell.backends.node import NodeTreeRoot
from contextshell.backends.virtual import VirtualTree
from contextshell.command import CommandInterpreter
from contextshell.path import NodePath
from contextshell.shell import Shell


class ShellScriptTestsBase(unittest.TestCase, ABC):
    @abstractmethod
    def create_shell(self) -> Shell:
        raise NotImplementedError()


class TreeRootTestsBase(ShellScriptTestsBase):
    @abstractmethod
    def create_tree_root(self):
        raise NotImplementedError()

    def create_shell(self):
        self.tree_root = self.create_tree_root()
        self.configure_tree_root(self.tree_root)

        interpreter = CommandInterpreter(self.tree_root)
        shell = Shell(interpreter)
        return shell

    def configure_tree_root(self, tree_root):
        pass


# TODO: is this class needed when testing single TreeRoot-based class?
class VirtualTreeTestsBase(TreeRootTestsBase):
    def create_tree_root(self):
        return VirtualTree()

    def configure_tree_root(self, tree_root):
        self.configure_virtual_tree(tree_root)

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
