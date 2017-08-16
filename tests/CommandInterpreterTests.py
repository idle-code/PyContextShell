import unittest

from contextshell.Command import Command
from contextshell.TreeRoot import TreeRoot
from contextshell.CommandInterpreter import CommandInterpreter


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
        set_cmd.target = 'foo'
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
        self.session.create('.foo.name', "foo")

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

if __name__ == '__main__':
    unittest.main()
