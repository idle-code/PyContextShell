import unittest
from unittest.mock import MagicMock, Mock, call

from contextshell.session_stack.SessionStack import *


class SessionStackTests(unittest.TestCase):
    def setUp(self):
        self.storage_mock = MagicMock()
        self.mock_manager = Mock()
        self.mock_manager.attach_mock(self.storage_mock, 'storage')
        self.mock_manager.attach_mock(MagicMock(), 'top')
        self.stack = SessionStack(self.storage_mock)

    def test_no_storage_layer(self):
        with self.assertRaises(ValueError):
            SessionStack(None)

    def test_start(self):
        self.storage_mock.start = MagicMock()
        self.stack.start(None)
        self.storage_mock.start.assert_called_once_with(None)

    def test_start_order(self):
        self.stack.push(self.mock_manager.top)
        self.stack.start(None)

        expected_call_order = [
            call.storage.start(None),
            call.top.start(self.storage_mock)
        ]
        self.assertListEqual(expected_call_order, self.mock_manager.mock_calls)

    def test_start_with_bottom_layer(self):
        with self.assertRaises(ValueError):
            self.stack.start(MagicMock())

    def test_finish_order(self):
        self.stack.push(self.mock_manager.top)
        self.stack.finish()

        expected_call_order = [
            call.top.finish(),
            call.storage.finish()
        ]
        self.assertListEqual(expected_call_order, self.mock_manager.mock_calls)

    def test_push_none(self):
        with self.assertRaises(ValueError):
            self.stack.push(None)

    def test_pop(self):
        layer = MagicMock()
        self.stack.push(layer)

        popped_layer = self.stack.pop()
        self.assertIs(popped_layer, layer)

    def test_pop_bottom(self):
        with self.assertRaises(RuntimeError):
            self.stack.pop()

    def _test_forwarding(self, method_name: str, expected_return, *args):
        method_mock = MagicMock(return_value=expected_return)
        self.storage_mock.attach_mock(method_mock, method_name)
        ret = getattr(self.stack, method_name)(*args)
        self.assertEqual(ret, expected_return)
        method_mock.assert_called_once_with(*args)

    def test_get_forwarding(self):
        self._test_forwarding('get', "BAR", '.foo')

    def test_set_forwarding(self):
        self._test_forwarding('set', None, '.foo', 321)

    def test_list_forwarding(self):
        self._test_forwarding('list', [NodePath('.foo'), NodePath('.bar')], '.')

    def test_exists_forwarding(self):
        self._test_forwarding('exists', False, '.spam')

    def test_create_forwarding(self):
        self._test_forwarding('create', None, '.spam', 123)

    def test_remove_forwarding(self):
        self._test_forwarding('remove', None, '.spam')


if __name__ == '__main__':
    unittest.main()
