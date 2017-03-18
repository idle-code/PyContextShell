import unittest
from CommandInterpreter import CommandInterpreter
from Command import Command
from Node import Node
from ActionNode import ActionNode


class GetAction(ActionNode):
    def __init__(self):
        super(GetAction, self).__init__()

    def __call__(self, target: Node, *arguments):
        return target.value


class SetAction(ActionNode):
    def __init__(self):
        super(SetAction, self).__init__()

    def __call__(self, target: Node, *arguments):
        target.value = arguments[0]


class CommandInterpreterTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.interpreter = CommandInterpreter(self.root)

        self.root.append_node("foo", Node(1))
        self.root['foo'].append_node("bar", Node(2))
        self.root.append_node("spam", Node('test'))

        # Create 'get' and 'set' actions just for 'foo' branch
        self.root['foo'].append_node(self.interpreter.actions_branch_path, Node())
        foo_actions = self.root['foo'][self.interpreter.actions_branch_path]
        foo_actions.append_node('get', GetAction())
        foo_actions.append_node('set', SetAction())

    def test_find_action(self):
        from_root_node = self.interpreter.find_action(self.interpreter.root, 'get')
        self.assertIsNone(from_root_node)

        from_foo_node = self.interpreter.find_action(self.interpreter.root['foo'], 'get')
        foo = self.root['foo']
        foo_actions = foo[self.interpreter.actions_branch_path]
        foo_actions_get = foo_actions['get']
        self.assertIs(from_foo_node, foo_actions_get)

        from_bar_node = self.interpreter.find_action(self.interpreter.root['foo.bar'], 'get')
        self.assertIs(from_bar_node, from_foo_node)

    def test_execute_get(self):
        get_cmd = Command('get')
        get_cmd.target = 'foo'
        foo_val = self.interpreter.execute(get_cmd)
        self.assertEqual(1, foo_val)

        get_cmd.target = 'foo.bar'
        bar_val = self.interpreter.execute(get_cmd)
        self.assertEqual(2, bar_val)

        get_cmd.target = 'spam'
        with self.assertRaises(NameError):
            self.interpreter.execute(get_cmd)

    def test_execute_set(self):
        set_cmd = Command('set')
        set_cmd.target = 'foo'
        set_cmd.arguments = [3]
        self.assertEqual(1, self.interpreter.root['foo'].value)
        self.interpreter.execute(set_cmd)
        self.assertEqual(3, self.interpreter.root['foo'].value)

        self.assertEqual(2, self.interpreter.root['foo.bar'].value)
        set_cmd.target = 'foo.bar'
        self.interpreter.execute(set_cmd)
        self.assertEqual(3, self.interpreter.root['foo.bar'].value)

    def test_unknown_target(self):
        get_cmd = Command('get')
        get_cmd.target = 'rabarbar'
        with self.assertRaises(NameError):
            self.interpreter.execute(get_cmd)

    def test_unknown_action(self):
        unknown_cmd = Command('unknown')
        with self.assertRaises(NameError):
            self.interpreter.execute(unknown_cmd)

    def test_recursive_target_evaluation(self):
        self.root['foo'].append_node('name', Node('foo'))
        # TODO: check why following doesnt't work:
        # self.root.append_node('foo.name', Node('foo'))

        get_name_cmd = Command('get')
        get_name_cmd.target = 'foo.name'

        get_cmd = Command('get')
        get_cmd.target = get_name_cmd

        # Execute: {foo.name: get}: get
        foo_val = self.interpreter.execute(get_cmd)
        self.assertEqual(foo_val, self.root['foo'].value)

    def test_recursive_action_evaluation(self):
        self.root['foo'].append_node('action', Node('get'))

        get_action_cmd = Command('get')
        get_action_cmd.target = 'foo.action'
        get_cmd = Command(get_action_cmd)
        get_cmd.target = 'foo'

        # Execute: foo: {foo.action: get}
        foo_val = self.interpreter.execute(get_cmd)
        self.assertEqual(foo_val, self.root['foo'].value)

    def test_recursive_argument_evaluation(self):
        self.root['foo'].append_node('value', Node(123))

        get_value_cmd = Command('get')
        get_value_cmd.target = 'foo.value'

        set_cmd = Command('set')
        set_cmd.target = 'foo'
        set_cmd.arguments = [get_value_cmd]

        # Execute: foo: set {foo.value: get}
        self.interpreter.execute(set_cmd)
        self.assertEqual(123, self.root['foo'].value)

if __name__ == '__main__':
    unittest.main()
