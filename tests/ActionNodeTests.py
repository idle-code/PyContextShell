import unittest

from ActionNode import *


class CustomNode(PyNode):
    def __init__(self):
        super().__init__()
        self.sample_action_value = "sample_action"
        self.named_value = "named"
        self.nested_value = "nested"
        self.subaction_value = "subaction"

    def _validate_args(self, target, args):
        if not isinstance(target, Node):
            raise TypeError('target is required to be Node but is ' + repr(target))

        for arg in args:
            if not isinstance(arg, Node):
                raise TypeError('arguments are required to be Node but one is ' + repr(arg))

    @action
    def sample_action(self, target: Node, *args: [Node]):
        self._validate_args(target, args)

        return self.sample_action_value

    @action(path='named')
    def named(self, target: Node, *args: [Node]):
        self._validate_args(target, args)

        return self.named_value

    @action(path='very.much.nested')
    def nested(self, target: Node, *args: [Node]):
        self._validate_args(target, args)

        return self.nested_value

    @action(path='named.subaction')
    def subaction(self, target: Node, *args: [Node]):
        self._validate_args(target, args)

        return self.subaction_value


class ActionNodeTests(unittest.TestCase):
    def setUp(self):
        self.node = CustomNode()

    def _test_node(self, action_name, result):
        self.assertTrue(self.node.contains('@actions'))
        actions_node = self.node['@actions']
        self.assertTrue(actions_node.contains(action_name))

        action_node = actions_node[action_name]
        self.assertEqual(result, action_node(self.node))
        self.assertEqual(result, action_node(self.node, Node(1), Node("test"), Node(None)))
        self.assertEqual(result, action_node(self.node, 1, "test", None))

    def _test_method(self, method, result):
        self.assertTrue(hasattr(self.node, method.__name__))

        self.assertEqual(result, method(self.node))
        self.assertEqual(result, method(self.node, Node(1), Node("test"), Node(None)))
        self.assertEqual(result, method(self.node, 1, "test", None))

    def test_action_node(self):
        self._test_node('sample_action', 'sample_action')

    def test_action_method(self):
        self._test_method(self.node.sample_action, 'sample_action')

    def test_named_node(self):
        self._test_node('named', 'named')

    def test_named_method(self):
        self._test_method(self.node.named, 'named')

    def test_nested_node(self):
        self.assertTrue(self.node.contains('@actions'))

        actions_node = self.node['@actions']
        self.assertTrue(actions_node.contains('very'))
        self.assertTrue(actions_node['very'].contains('much'))
        self.assertTrue(actions_node['very']['much'].contains('nested'))

        nested_node = actions_node['very']['much']['nested']
        self.assertEqual("nested", nested_node(self.node))
        self.assertEqual("nested", nested_node(self.node, Node(1), Node("test"), Node(None)))
        self.assertEqual("nested", nested_node(self.node, 1, "test", None))

    def test_nested_method(self):
        self._test_method(self.node.nested, 'nested')

    def test_subaction_node(self):
        self.test_named_node()

        actions_node = self.node['@actions']
        self.assertTrue(actions_node.contains('named'))
        self.assertTrue(actions_node['named'].contains('subaction'))

        subaction_node = actions_node['named']['subaction']
        self.assertEqual("subaction", subaction_node(self.node))
        self.assertEqual("subaction", subaction_node(self.node, Node(1), Node("test"), Node(None)))
        self.assertEqual("subaction", subaction_node(self.node, 1, "test", None))

    def test_subaction_method(self):
        self._test_method(self.node.subaction, 'subaction')

if __name__ == '__main__':
    unittest.main()

