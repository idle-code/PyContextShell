import unittest
from BasicActions import *


class ActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.root.append('foo', Node(1))
        self.root.append('bar', Node(2))
        self.root['foo'].append('spam', Node("SPAM"))


class GetTests(ActionTests):
    def setUp(self):
        super().setUp()
        self.get = GetAction()

    def test_get(self):
        self.assertEqual(1, self.get(self.root['foo']))
        self.assertEqual(2, self.get(self.root['bar']))
        self.assertEqual("SPAM", self.get(self.root['foo']['spam']))

    def test_get_any_arguments(self):
        with self.assertRaises(ArgumentError):
            self.get(self.root, 1, 2, 3)


class SetTests(ActionTests):
    def setUp(self):
        super().setUp()
        self.set = SetAction()

    def test_set(self):
        self.assertEqual(1, self.root['foo'].get())
        self.set(self.root['foo'], 6)
        self.assertEqual(6, self.root['foo'].get())

    def test_set_no_argument(self):
        with self.assertRaises(ArgumentError):
            self.set(self.root['foo'])

    def test_set_too_many_arguments(self):
        with self.assertRaises(ArgumentError):
            self.set(self.root['foo'], 1, 2, 3)


class ListTests(ActionTests):
    def setUp(self):
        super().setUp()
        self.list = ListAction()

    def test_list(self):
        root_list = self.list(self.root)
        self.assertListEqual(['foo', 'bar'], root_list)

        foo_list = self.list(self.root['foo'])
        self.assertListEqual(['spam'], foo_list)

        bar_list = self.list(self.root['bar'])
        self.assertListEqual([], bar_list)

    def test_list_any_arguments(self):
        with self.assertRaises(ArgumentError):
            self.list(self.root, 1, 2, 3)


class RemoveTests(ActionTests):
    def setUp(self):
        super().setUp()
        self.remove = RemoveAction()

    def test_remove_existing(self):
        self.assertTrue(self.root.contains('bar'))
        self.remove(self.root, 'bar')
        self.assertFalse(self.root.contains('bar'))

    @unittest.skip("Check if this behavior is necessary")
    def test_remove_many_existing(self):
        self.assertTrue(self.root.contains('foo'))
        self.assertTrue(self.root.contains('bar'))
        self.remove(self.root, 'foo', 'bar')
        self.assertFalse(self.root.contains('foo'))
        self.assertFalse(self.root.contains('bar'))

    def test_remove_nonexistent(self):
        with self.assertRaises(NameError):
            self.remove(self.root, 'rabarbar')

    def test_remove_no_argument(self):
        with self.assertRaises(ArgumentError):
            self.remove(self.root)


class CreateTests(ActionTests):
    def setUp(self):
        super().setUp()
        self.create = CreateAction()

    def test_create_default_value(self):
        self.assertFalse(self.root.contains('rabarbar'))
        self.create(self.root, 'rabarbar')
        self.assertTrue(self.root.contains('rabarbar'))
        self.assertIsNone(self.root['rabarbar'].get())

    def test_create_specified_value(self):
        self.assertFalse(self.root.contains('rabarbar'))
        self.create(self.root, 'rabarbar', 12)
        self.assertTrue(self.root.contains('rabarbar'))
        self.assertEqual(12, self.root['rabarbar'].get())

    def test_create_existing(self):
        with self.assertRaises(NameError):
            self.create(self.root, 'foo')

    def test_create_no_argument(self):
        with self.assertRaises(ArgumentError):
            self.create(self.root)

    def test_create_too_many_arguments(self):
        with self.assertRaises(ArgumentError):
            self.create(self.root, 'name', 'val', 'more')


if __name__ == '__main__':
    unittest.main()
