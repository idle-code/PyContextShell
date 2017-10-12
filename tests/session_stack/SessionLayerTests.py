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
        super().__init__()
        self.action_name = 'not called'
        self.target = 'no target'
        self.received_arguments = None
        self.return_value = None

    def remember_arguments(self, action_name, target, *args):
        self.action_name = action_name
        self.target = target
        self.received_arguments = list(args)
        return self.return_value

    def get(self, target: NodePath, *args):
        return self.remember_arguments('get', target, *args)

    def set(self, target: NodePath, *args):
        return self.remember_arguments('set', target, *args)

    def list(self, target: NodePath, *args):
        return self.remember_arguments('list', target, *args)

    def exists(self, target: NodePath, *args):
        return self.remember_arguments('exists', target, *args)

    def create(self, target: NodePath, *args):
        return self.remember_arguments('create', target, *args)

    def remove(self, target: NodePath, *args):
        return self.remember_arguments('remove', target, *args)


class FakeLayer(SessionLayer):
    def __init__(self):
        self.target = 'no target'
        self.action_name = 'not called'
        self.args = tuple()
        self.execute_return_value = None

    def execute(self, target: NodePath, action_name: NodePath, *args):
        self.target = target
        self.action_name = action_name
        self.args = args
        return self.execute_return_value


class MethodToExecuteFakeLayer(CrudSessionLayer):
    def __init__(self):
        self.next_layer = FakeLayer()

    @property
    def target(self):
        return self.next_layer.target

    @property
    def action_name(self):
        return self.next_layer.action_name

    @property
    def args(self):
        return self.next_layer.args


class CrudSessionLayerExecuteForwardingTests(unittest.TestCase):
    def check_execute_forwards_to_method(self, action_name):
        layer = ExecuteToMethodFakeLayer()
        layer.return_value = 123
        target_path = NodePath('foo.bar')
        passed_arguments = [1, 2, 'spam']

        return_value = layer.execute(target_path, action_name, *passed_arguments)

        self.assertEqual(layer.target, target_path)
        self.assertEqual(layer.action_name, action_name)
        self.assertListEqual(list(layer.received_arguments), passed_arguments)
        self.assertEqual(return_value, layer.return_value)

    def check_execute_forwards_to_next_layer(self, action_name):
        fake_next_layer = FakeLayer()
        fake_next_layer.execute_return_value = 123
        layer = CrudSessionLayer()
        layer.next_layer = fake_next_layer
        target_path = NodePath('foo.bar')
        passed_arguments = [1, 2, 'spam']

        return_value = layer.execute(target_path, action_name, *passed_arguments)

        self.assertEqual(fake_next_layer.target, target_path)
        self.assertEqual(fake_next_layer.action_name, action_name)
        self.assertListEqual(list(fake_next_layer.args), passed_arguments)
        self.assertEqual(return_value, fake_next_layer.execute_return_value)

    def test_execute_forwards_to_next_layer(self):
        self.check_execute_forwards_to_next_layer('other.method')

    def test_executing_execute_forwards_to_next_layer(self):
        self.check_execute_forwards_to_next_layer('execute')

    def test_execute_forwards_to_get(self):
        self.check_execute_forwards_to_method('get')

    def test_execute_forwards_to_set(self):
        self.check_execute_forwards_to_method('set')

    def test_execute_forwards_to_list(self):
        self.check_execute_forwards_to_method('list')

    def test_execute_forwards_to_exists(self):
        self.check_execute_forwards_to_method('exists')

    def test_execute_forwards_to_create(self):
        self.check_execute_forwards_to_method('create')

    def test_execute_forwards_to_remove(self):
        self.check_execute_forwards_to_method('remove')


class CrudSessionLayerMethodForwardingTests(unittest.TestCase):
    def check_forwarding_to_execute(self, action_name: str, *args):
        layer = MethodToExecuteFakeLayer()
        target = NodePath('foo.bar')

        tested_method = getattr(layer, action_name)
        tested_method(target, *args)

        self.assertEqual(layer.target, target)
        self.assertEqual(layer.action_name, action_name)
        self.assertListEqual(list(layer.args), list(args))

    def test_get_forwards_to_execute(self):
        self.check_forwarding_to_execute('get')

    def test_set_forwards_to_execute(self):
        self.check_forwarding_to_execute('set', 3)

    def test_list_forwards_to_execute(self):
        self.check_forwarding_to_execute('list')
        self.check_forwarding_to_execute('list', NodePath('spam'))

    def test_exists_forwards_to_execute(self):
        self.check_forwarding_to_execute('exists', NodePath('spam'))

    def test_create_forwards_to_execute(self):
        self.check_forwarding_to_execute('create', NodePath('spam'))

    def test_create_with_value_forwards_to_execute(self):
        self.check_forwarding_to_execute('create', NodePath('spam'), 123)

    def test_remove_forwards_to_execute(self):
        self.check_forwarding_to_execute('remove', NodePath('spam'))


if __name__ == '__main__':
    unittest.main()
