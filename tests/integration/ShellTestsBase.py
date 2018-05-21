from integration.ScriptTestBase import ScriptTestBase


class ShellTestsBase(ScriptTestBase):
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

        def get(tree: Tree, target: NodePath, action: NodePath):
            return tree.get(target)

        finder.install_action(".", "get", get)

        def set(tree: Tree, target: NodePath, action: NodePath, new_value):
            return tree.set(target, new_value)

        finder.install_action(".", "set", set)

        def list(tree: Tree, target: NodePath, action: NodePath):
            return tree.list(target)

        finder.install_action(".", "list", list)

        def remove(tree: Tree, target: NodePath, action: NodePath):
            return tree.remove(target)

        finder.install_action(".", "remove", remove)