import unittest

from ActionNode import Action
from Node import Node
from PyNode import PyNode


class PythonicNode(PyNode):
    def __init__(self):
        super().__init__()

    @Action
    def return_42(self):
        return 42

    @Action
    def add_one(self, value: Node):
        return value.value + 1

    @Action
    def return_args(self, *args: [Node]):
        return map(lambda n: n.value, args)

    @Action
    def return_target_value(self, target: Node):
        return target.value

    @Action
    def set_target_value(self, target: Node, new_value: Node):
        target.value = new_value.value + 3


class PythonicAccessTests(unittest.TestCase):
    def setUp(self):
        self.node = PythonicNode()
        self.node.append_node('child', Node())  # Child should not have parent's methods

    @unittest.skip("Check if needed")
    def test_call_return(self):
        self.assertEqual(42, self.node.return_42())

    @unittest.skip("Check if needed")
    def test_call_single_argument(self):
        self.assertEqual(42, self.node.add_one(41))

    @unittest.skip("Check if needed")
    def test_call_multiple_arguments(self):
        self.assertListEqual([1, 2, 3, 4], self.node.return_args(1, 2, 3, 4))

    @unittest.skip("Check if needed")
    def test_call_target(self):
        self.node.value = 456
        self.assertEqual(456, self.node.return_target_value())

        self.node['child'].value = 789
        self.assertEqual(789, self.node['child'].return_target_value())

    @unittest.skip("Check if needed")
    def test_call_target_with_arguments(self):
        self.node.set_target_value(1)
        self.assertEqual(1 + 3, self.node.value)

        self.node['child'].set_target_value(4)
        self.assertEqual(4 + 3, self.node['child'].value)


class ActionNodeNodeAccessTests(unittest.TestCase):
    def setUp(self):
        self.node = PythonicNode()
        self.node.append_node('child', Node())  # Child should not have parent's methods

    @unittest.skip("Not implemented")
    def test_call_return(self):
        #self.assertEqual(42, self.node)
        pass

    @unittest.skip("Not implemented")
    def test_call_single_argument(self):
        #self.assertEqual(42, self.node.add_one(41))
        pass

    @unittest.skip("Not implemented")
    def test_call_multiple_arguments(self):
        #self.assertListEqual([1, 2, 3, 4], self.node.return_args(1, 2, 3, 4))
        pass

    @unittest.skip("Not implemented")
    def test_call_target(self):
        self.node.value = 456
        #self.assertEqual(456, self.node.return_target_value())

        self.node['child'].value = 789
        #self.assertEqual(789, self.node['child'].return_target_value())

    @unittest.skip("Not implemented")
    def test_call_target_with_arguments(self):
        #self.node.set_target_value(1)
        self.assertEqual(1 + 3, self.node.value)

        #self.node['child'].set_target_value(4)
        self.assertEqual(4 + 3, self.node['child'].value)