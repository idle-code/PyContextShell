import unittest

from contextshell.Node import Node
from contextshell.NodePath import NodePath
from contextshell.session_stack.SessionStack import SessionStack
from contextshell.session_stack.StorageLayer import StorageLayer
from contextshell.session_stack.SessionLayer import SessionLayer
from contextshell.Command import Command
from contextshell.TreeRoot import TreeRoot
from contextshell.CommandInterpreter import CommandInterpreter
from contextshell.ActionNode import ActionNode


class CommandInterpreterTests(unittest.TestCase):
    def setUp(self):
        root = TreeRoot()
        self.session = root.create_session()
        self.interpreter = CommandInterpreter(self.session)

        self.session.create('.foo', 1)
        self.session.create('.foo.bar', 2)
        self.session.create('.spam', "test")

    def test_execute_get(self):
        get_cmd = Command('get')
        get_cmd.target = '.foo'
        foo_val = self.interpreter.execute(get_cmd)
        self.assertEqual(1, foo_val)

        get_cmd.target = '.foo.bar'
        bar_val = self.interpreter.execute(get_cmd)
        self.assertEqual(2, bar_val)

        get_cmd.target = '.spam'
        spam_val = self.interpreter.execute(get_cmd)
        self.assertEqual('test', spam_val)

    def test_execute_set(self):
        set_cmd = Command('set')
        set_cmd.target = '.foo'
        set_cmd.arguments = [3]
        self.interpreter.session.get('.foo')
        self.assertEqual(1, self.interpreter.session.get('.foo'))
        self.interpreter.execute(set_cmd)
        self.assertEqual(3, self.interpreter.session.get('.foo'))

        self.assertEqual(2, self.interpreter.session.get('.foo.bar'))
        set_cmd.target = '.foo.bar'
        self.interpreter.execute(set_cmd)
        self.assertEqual(3, self.interpreter.session.get('.foo.bar'))

    def test_unknown_target(self):
        get_cmd = Command('get')
        get_cmd.target = '.rabarbar'
        with self.assertRaises(NameError):
            self.interpreter.execute(get_cmd)

    def test_unknown_action(self):
        unknown_cmd = Command('unknown')
        with self.assertRaises(NameError):
            self.interpreter.execute(unknown_cmd)

    def test_recursive_target_evaluation(self):
        self.session.create('.foo.name', ".foo")

        get_name_cmd = Command('get')
        get_name_cmd.target = '.foo.name'

        get_cmd = Command('get')
        get_cmd.target = get_name_cmd

        # Execute:
        #   {foo.name: get}: get
        foo_val = self.interpreter.execute(get_cmd)
        self.assertEqual(foo_val, self.session.get('.foo'))

    def test_recursive_action_evaluation(self):
        self.session.create('.foo.action', "get")

        get_action_cmd = Command('get')
        get_action_cmd.target = '.foo.action'
        get_cmd = Command(get_action_cmd)
        get_cmd.target = '.foo'

        # Execute:
        #   foo: {foo.action: get}
        foo_val = self.interpreter.execute(get_cmd)
        self.assertEqual(foo_val, self.session.get('.foo'))

    def test_recursive_argument_evaluation(self):
        self.session.create('.foo.value', 123)

        get_value_cmd = Command('get')
        get_value_cmd.target = '.foo.value'

        set_cmd = Command('set')
        set_cmd.target = '.foo'
        set_cmd.arguments = [get_value_cmd]

        # Execute:
        #   foo: set {foo.value: get}
        self.interpreter.execute(set_cmd)
        self.assertEqual(123, self.session.get('.foo'))


class CommandLookupTests(unittest.TestCase):
    class ReturnAction(ActionNode):
        def __init__(self, name: str, return_value):
            super().__init__(NodePath(name))
            self.return_value = return_value

        def __call__(self, session: SessionLayer, target: NodePath, *arguments):
            return self.return_value

    def setUp(self):
        root = TreeRoot()
        self.session = root.create_session()
        self.interpreter = CommandInterpreter(self.session)

        self.session.create('.foo', 1)
        self.session.create('.foo.bar', 2)
        root.install_action(CommandLookupTests.ReturnAction('num', 'ROOT'))
        root.install_action(CommandLookupTests.ReturnAction('num', 'FOO'), 'foo')
        root.install_action(CommandLookupTests.ReturnAction('num', 'BAR'), 'foo.bar')
        root.install_action(CommandLookupTests.ReturnAction('sesnum', 'SESSION'), 'session')

    def test_hierarchy_lookup(self):
        num_cmd = Command('num')
        num_cmd.target = NodePath('.')
        self.assertEqual(self.interpreter.execute(num_cmd), 'ROOT')

        num_cmd.target = NodePath('.foo')
        self.assertEqual(self.interpreter.execute(num_cmd), 'FOO')

        num_cmd.target = NodePath('.foo.bar')
        self.assertEqual(self.interpreter.execute(num_cmd), 'BAR')

        num_cmd.target = NodePath('.session')
        self.assertEqual(self.interpreter.execute(num_cmd), 'ROOT')

    def test_alternative_lookup(self):
        sesnum_cmd = Command('sesnum')
        sesnum_cmd.target = NodePath('.')
        self.assertEqual(self.interpreter.execute(sesnum_cmd), 'SESSION')

        sesnum_cmd.target = NodePath('.foo.bar')
        self.assertEqual(self.interpreter.execute(sesnum_cmd), 'SESSION')

        sesnum_cmd.target = NodePath('.session')
        self.assertEqual(self.interpreter.execute(sesnum_cmd), 'SESSION')


if __name__ == '__main__':
    unittest.main()

