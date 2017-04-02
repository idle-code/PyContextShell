import unittest

from ActionNode import *


def sum_function(target: Node, number: int):
    return target.get() + number


class ActionNodeTests(unittest.TestCase):
    def setUp(self):
        self.target = Node(3)
        self.empty_node = ActionNode()
        self.sum_node = ActionNode(sum_function)

    def test_empty_action(self):
        with self.assertRaises(NotImplementedError):
            self.empty_node(self.target, 1, 2, 3)

    def test_from_function(self):
        six = self.sum_node(self.target, 3)
        self.assertEqual(6, six)

    def test_from_subclass(self):
        class DiffActionNode(ActionNode):
            def __call__(self, target: Node, number: int):
                return target.get() - number

        self.diff_node = DiffActionNode()

        two = self.diff_node(self.target, 1)
        self.assertEqual(2, two)


if __name__ == '__main__':
    unittest.main()

