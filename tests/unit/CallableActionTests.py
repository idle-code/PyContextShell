import unittest
from unittest.mock import Mock, ANY
from contextshell.NodePath import NodePath as np
from collections import OrderedDict


def create_action(implementation, name='action'):  # FIXME: ugly; add tests for name parameter
    from contextshell.CallableAction import CallableAction
    return CallableAction(implementation, np(name))


class CallTests(unittest.TestCase):
    def test_target_path_is_passed(self):
        implementation = Mock()
        action = create_action(implementation)

        action.invoke(np('.target'), np('action'), OrderedDict())

        self.assertIn(np('.target'), *implementation.call_args)

    def test_arguments_are_unpacked_to_list(self):
        implementation = Mock()
        action = create_action(implementation)
        arguments = OrderedDict([
            (0, 'foo'),
            (1, 'bar'),
            ])

        action.invoke(np('.target'), np('action'), arguments)

        implementation.assert_called_with(ANY, 'foo', 'bar')

    def test_arguments_are_unpacked_to_keywords(self):
        implementation = Mock()
        action = create_action(implementation)
        arguments = OrderedDict([
            (np('foo'), 'spam'),
            (np('bar'), 2),
            ])

        action.invoke(np('.target'), np('action'), arguments)

        implementation.assert_called_with(ANY, foo='spam', bar=2)

    def test_return_value_is_forwarded(self):
        implementation = Mock()
        implementation.return_value = 'VALUE'
        action = create_action(implementation)

        action_result = action.invoke(np('.target'), np('action'), OrderedDict())

        self.assertEqual('VALUE', action_result)
