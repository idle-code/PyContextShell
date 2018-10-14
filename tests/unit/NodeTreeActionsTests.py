import unittest
from typing import Dict, Union, Any

from contextshell.NodePath import NodePath as np
from contextshell.NodePath import NodePath
from contextshell.ActionEndpoint import ActionEndpoint


# class ActionTests(unittest.TestCase):
#     pass
#
#
# class CreateActionTests(ActionTests):
#     def create_tree(self):
#         from contextshell.NodeTreeRoot import NodeTreeRoot
#         return NodeTreeRoot()
#
#     def test_create_no_value(self):
#         tree = self.create_tree()
#
#         tree.create_action(np('.'), 'foo')
#
#         foo_exists = tree.exists(np('.foo'))
#         self.assertTrue(foo_exists)
