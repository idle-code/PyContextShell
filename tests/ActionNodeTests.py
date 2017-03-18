import unittest

from ActionNode import *


class CustomNode(PyNode):
    def __init__(self):
        super().__init__()
        self.action_value = "action"
        self.named_value = "named"
        self.nested_value = "nested"
        self.subaction_value = "subaction"

    def _validate_args(self, target, args):
        if not isinstance(target, Node):
            raise TypeError('target is required to be Node but is ' + repr(target))

        for arg in args:
            if not isinstance(arg, Node):
                raise TypeError('arguments are required to be Node but one is ' + repr(arg))

    @Action
    def action(self, target: Node, *args: [Node]):
        self._validate_args(target, args)

        return self.action_value

    @Action(path='named')
    def named(self, target: Node, *args: [Node]):
        self._validate_args(target, args)

        return self.named_value

    @Action(path='very.much.nested')
    def nested(self, target: Node, *args: [Node]):
        self._validate_args(target, args)

        return self.nested_value

    @Action(path='named.subaction')
    def subaction(self, target: Node, *args: [Node]):
        self._validate_args(target, args)

        return self.subaction_value


class ActionNodeTests(unittest.TestCase):
    def setUp(self):
        self.node = CustomNode()

    def _test_node(self, action_name, result):
        self.assertTrue('@actions' in self.node.subnode_names)

        actions_node = self.node['@actions']
        self.assertIn(action_name, list(actions_node.subnode_names))

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
        self._test_node('action', 'action')

    def test_action_method(self):
        self._test_method(self.node.action, 'action')

    def test_named_node(self):
        self._test_node('named', 'named')

    def test_named_method(self):
        self._test_method(self.node.named, 'named')

    def test_nested_node(self):
        self.assertTrue('@actions' in self.node.subnode_names)

        actions_node = self.node['@actions']
        self.assertTrue('very' in actions_node.subnode_names)
        self.assertTrue('much' in actions_node['very'].subnode_names)
        self.assertTrue('nested' in actions_node['very']['much'].subnode_names)

        nested_node = actions_node['very']['much']['nested']
        self.assertEqual("nested", nested_node(self.node))
        self.assertEqual("nested", nested_node(self.node, Node(1), Node("test"), Node(None)))
        self.assertEqual("nested", nested_node(self.node, 1, "test", None))

    def test_nested_method(self):
        self._test_method(self.node.nested, 'nested')

    def test_subaction_node(self):
        self.test_named_node()

        actions_node = self.node['@actions']
        self.assertTrue('named' in actions_node.subnode_names)
        self.assertTrue('subaction' in actions_node['named'].subnode_names)

        subaction_node = actions_node['named']['subaction']
        self.assertEqual("subaction", subaction_node(self.node))
        self.assertEqual("subaction", subaction_node(self.node, Node(1), Node("test"), Node(None)))
        self.assertEqual("subaction", subaction_node(self.node, 1, "test", None))

    def test_subaction_method(self):
        self._test_method(self.node.subaction, 'subaction')

if __name__ == '__main__':
    unittest.main()

