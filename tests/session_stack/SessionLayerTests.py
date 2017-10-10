import unittest
from unittest.mock import MagicMock
from contextshell.session_stack.CrudSessionLayer import CrudSessionLayer
from tests.session_stack.TestBases import TestBases
from contextshell.session_stack.CrudSessionLayer import SessionLayer
from contextshell.NodePath import NodePath


class SessionLayerTests(unittest.TestCase):
    def test_execute_forward_args(self):
        fake_layer = MagicMock()
        fake_layer.execute = MagicMock()
        session_layer = SessionLayer()
        session_layer.next_layer = fake_layer

        target_path = NodePath('.foo.bar')
        session_layer.execute(target_path, 'spam', 1, 2, 3)

        fake_layer.execute.assert_called_once_with(target_path, 'spam', 1, 2, 3)

    def test_execute_return_forward_return(self):
        fake_layer = MagicMock()
        fake_layer.execute = MagicMock()
        fake_layer.execute.side_effect = ['rabarbar']
        session_layer = SessionLayer()
        session_layer.next_layer = fake_layer

        return_value = session_layer.execute(NodePath('.foo.bar'), 'spam')

        self.assertEqual('rabarbar', return_value)

# class SessionLayerTests(TestBases.SessionLayerTestsBase):
#     def prepare_layer(self, session: CrudSessionLayer) -> CrudSessionLayer:
#         return CrudSessionLayer()


class ExecuteToMethodFakeLayer(CrudSessionLayer):
    def __init__(self):
        self.action_name = 'not called'
        self.received_arguments = None
        self.return_value = None

    def check_arguments(self, action_name, *args):
        self.action_name = action_name
        self.received_arguments = list(args)
        return self.return_value

    def get(self, path: NodePath):
        return self.check_arguments('get', path)

    def set(self, path: NodePath, new_value):
        return self.check_arguments('set', path, new_value)

    def list(self, path: NodePath):
        return self.check_arguments('list', path)

    def exists(self, path: NodePath) -> bool:
        return self.check_arguments('exists', path)

    def create(self, path: NodePath, value=None):
        return self.check_arguments('create', path, value)

    def remove(self, path: NodePath):
        return self.check_arguments('remove', path)


class CrudSessionLayerExecuteForwardingTests(unittest.TestCase):
    def check_argument_forwarding(self, action_name, *args):
        session_layer = ExecuteToMethodFakeLayer()
        target_path = NodePath('foo.bar')

        session_layer.execute(target_path, action_name, *args)

        self.assertEqual(action_name, session_layer.action_name)
        self.assertListEqual([target_path] + list(args), session_layer.received_arguments)

    def check_target_in_argument_normalization(self, action_name, *args):
        session_layer = ExecuteToMethodFakeLayer()
        target_path = NodePath('foo.bar')
        target_in_argument = 'spam'

        session_layer.execute(target_path, action_name, target_in_argument, *args)

        self.assertEqual(action_name, session_layer.action_name)
        self.assertListEqual([NodePath.join(target_path, target_in_argument)] + list(args),
                             session_layer.received_arguments)

    def check_return_value_forwarding(self, action_name, expected_return_value, *args):
        session_layer = ExecuteToMethodFakeLayer()
        session_layer.return_value = expected_return_value
        target_path = NodePath('foo.bar')

        return_value = session_layer.execute(target_path, action_name, *args)

        self.assertEqual(return_value, expected_return_value)

    def test_execute_forwards_to_get(self):
        self.check_argument_forwarding('get')

    @unittest.skip("Not sure if normalization should be done here")
    def test_execute_normalizes_get(self):
        self.check_target_in_argument_normalization('get')

    def test_execute_forwards_get_return_value(self):
        self.check_return_value_forwarding('get', 1)

    def test_execute_forwards_to_set(self):
        self.check_argument_forwarding('set', 1)

    def test_execute_forwards_to_list(self):
        self.check_argument_forwarding('list')

    @unittest.skip("Not sure if normalization should be done here")
    def test_execute_normalizes_list(self):
        self.check_target_in_argument_normalization('list')

    def test_execute_forwards_list_return_value(self):
        self.check_return_value_forwarding('list', ['foo', 'bar'])

    def test_execute_forwards_to_exists(self):
        session_layer = ExecuteToMethodFakeLayer()
        target_path = NodePath('foo.bar')
        path_to_check = NodePath('some.path')

        session_layer.execute(target_path, 'exists', path_to_check)

        self.assertEqual('exists', session_layer.action_name)
        self.assertListEqual(session_layer.received_arguments,
                             [NodePath.join(target_path, path_to_check)])

    def test_execute_forwards_exists_return_value(self):
        self.check_return_value_forwarding('exists', True, NodePath('some.path'))

    def test_execute_forwards_to_create_no_args(self):
        session_layer = ExecuteToMethodFakeLayer()
        target_path = NodePath('foo.bar')
        with self.assertRaises(RuntimeError):
            session_layer.execute(target_path, 'create')

    def test_execute_forwards_to_create_just_name(self):
        session_layer = ExecuteToMethodFakeLayer()
        target_path = NodePath('foo.bar')

        session_layer.execute(target_path, 'create', 'spam')

        self.assertEqual('create', session_layer.action_name)
        self.assertListEqual(session_layer.received_arguments,
                             [NodePath.join(target_path, 'spam'), None])

    def test_execute_forwards_to_create_name_and_value(self):
        session_layer = ExecuteToMethodFakeLayer()
        target_path = NodePath('foo.bar')

        session_layer.execute(target_path, 'create', 'spam', 1)

        self.assertEqual('create', session_layer.action_name)
        self.assertListEqual(session_layer.received_arguments,
                             [NodePath.join(target_path, 'spam'), 1])

    def test_execute_forwards_to_remove(self):
        session_layer = ExecuteToMethodFakeLayer()
        target_path = NodePath('foo.bar')

        session_layer.execute(target_path, 'remove', 'spam')

        self.assertEqual('remove', session_layer.action_name)
        self.assertListEqual(session_layer.received_arguments,
                             [NodePath.join(target_path, 'spam')])

    @unittest.skip("Not sure if normalization should be done here")
    def test_execute_normalizes_remove(self):
        self.check_target_in_argument_normalization('remove')


class MethodToExecuteFakeLayer(CrudSessionLayer):
    def __init__(self):
        self.target = 'no target'
        self.action_name = 'not called'
        self.args = tuple()

    def execute(self, target: NodePath, action_name: NodePath, *args):
        self.target = target
        self.action_name = action_name
        self.args = args


class CrudSessionLayerMethodForwardingTests(unittest.TestCase):
    def test_get_forwards_to_execute(self):
        session_layer = MethodToExecuteFakeLayer()
        target = NodePath('foo.bar')

        session_layer.get(target)

        self.assertEqual(session_layer.target, target)
        self.assertEqual(session_layer.action_name, 'get')
        self.assertListEqual(list(session_layer.args), [])

    def test_set_forwards_to_execute(self):
        session_layer = MethodToExecuteFakeLayer()
        target = NodePath('foo.bar')

        session_layer.set(target, 2)

        self.assertEqual(session_layer.target, target)
        self.assertEqual(session_layer.action_name, 'set')
        self.assertListEqual(list(session_layer.args), [2])

    def test_list_forwards_to_execute(self):
        session_layer = MethodToExecuteFakeLayer()
        target = NodePath('foo.bar')

        session_layer.list(target)

        self.assertEqual(session_layer.target, target)
        self.assertEqual(session_layer.action_name, 'list')
        self.assertListEqual(list(session_layer.args), [])

    def test_exists_forwards_to_execute(self):
        session_layer = MethodToExecuteFakeLayer()
        parent_path = NodePath('foo')
        arg_path = NodePath('bar')

        session_layer.exists(NodePath.join(parent_path, arg_path))

        self.assertEqual(session_layer.target, parent_path)
        self.assertEqual(session_layer.action_name, 'exists')
        self.assertListEqual(list(session_layer.args), [arg_path])

    def test_create_forwards_to_execute(self):
        session_layer = MethodToExecuteFakeLayer()
        parent_path = NodePath('foo')
        arg_path = NodePath('bar')

        session_layer.create(NodePath.join(parent_path, arg_path))

        self.assertEqual(session_layer.target, parent_path)
        self.assertEqual(session_layer.action_name, 'create')
        self.assertListEqual(list(session_layer.args), [arg_path])

    def test_create_with_value_forwards_to_execute(self):
        session_layer = MethodToExecuteFakeLayer()
        parent_path = NodePath('foo')
        arg_path = NodePath('bar')

        session_layer.create(NodePath.join(parent_path, arg_path), 3)

        self.assertEqual(session_layer.target, parent_path)
        self.assertEqual(session_layer.action_name, 'create')
        self.assertListEqual(list(session_layer.args), [arg_path, 3])

    def test_remove_forwards_to_execute(self):
        session_layer = MethodToExecuteFakeLayer()
        parent_path = NodePath('foo')
        arg_path = NodePath('bar')

        session_layer.remove(NodePath.join(parent_path, arg_path))

        self.assertEqual(session_layer.target, parent_path)
        self.assertEqual(session_layer.action_name, 'remove')
        self.assertListEqual(list(session_layer.args), [arg_path])


if __name__ == '__main__':
    unittest.main()
