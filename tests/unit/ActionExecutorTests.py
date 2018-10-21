import unittest
from collections import OrderedDict
from typing import Optional

from contextshell.action import Action, ActionExecutor, pack_argument_tree
from tests.unit.Fakes import FakeAction

from contextshell.path import NodePath, NodePath as np  # isort:skip


class TestableActionExecutor(ActionExecutor):
    found_action: Optional[Action] = None

    def find_action(self, target: NodePath, action: NodePath) -> Optional[Action]:
        return self.found_action


class ExecuteTests(unittest.TestCase):
    def test_no_action_found(self):
        executor = TestableActionExecutor()

        with self.assertRaises(NameError):
            executor.execute(np("target"), np("action"))

    def test_no_args_passes_empty_dict(self):
        executor = TestableActionExecutor()
        action = FakeAction()
        executor.found_action = action

        executor.execute(np("target"), action.name)

        self.assertEqual(OrderedDict(), action.received_arguments)

    def test_args_are_passed_to_action(self):
        executor = TestableActionExecutor()
        action = FakeAction()
        executor.found_action = action
        packed_args = pack_argument_tree('foo', 123)

        executor.execute(np("target"), action.name, packed_args)

        self.assertEqual(packed_args, action.received_arguments)
