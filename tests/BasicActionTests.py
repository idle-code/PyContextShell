import unittest
from Node import *
from BasicActions import BasicActions


class ActionTests(unittest.TestCase):
    def setUp(self):
        self.root = Node()
        self.foo = Node(1)
        self.root.append('foo', self.foo)
        self.bar = Node(2)
        self.root.append('bar', self.bar)
        self.spam = Node("SPAM")
        self.foo.append('spam', self.spam)


class GetTests(ActionTests):
    def test_get(self):
        self.assertEqual(1, BasicActions.get(self.foo))
        self.assertEqual(2, BasicActions.get(self.bar))
        self.assertEqual("SPAM", BasicActions.get(self.spam))

    def test_get_any_arguments(self):
        with self.assertRaises(TypeError):
            BasicActions.get(self.foo, 1, 2, 3)


class SetTests(ActionTests):
    def test_set(self):
        self.assertEqual(1, BasicActions.get(self.foo))
        BasicActions.set(self.foo, 6)
        self.assertEqual(6, BasicActions.get(self.foo))

    def test_set_no_value(self):
        with self.assertRaises(TypeError):
            BasicActions.set(self.foo)

    def test_set_too_many_arguments(self):
        with self.assertRaises(TypeError):
            BasicActions.set(self.foo, 1, 2, 3)


class ListTests(ActionTests):
    def test_list(self):
        root_list = BasicActions.list(self.root)
        self.assertListEqual(['foo', 'bar'], root_list)

        foo_list = BasicActions.list(self.foo)
        self.assertListEqual(['spam'], foo_list)

        bar_list = BasicActions.list(self.bar)
        self.assertListEqual([], bar_list)

    def test_list_any_arguments(self):
        with self.assertRaises(TypeError):
            BasicActions.list(self.root, 1, 2, 3)


class ExistsTests(ActionTests):
    def test_exist(self):
        self.assertTrue(BasicActions.exists(self.foo, 'spam'))

    def test_doesnt_exist(self):
        self.assertFalse(BasicActions.exists(self.root, 'rabarbar'))


class RemoveTests(ActionTests):
    def test_remove_existing(self):
        self.assertTrue(BasicActions.exists(self.root, 'bar'))
        BasicActions.remove(self.root, 'bar')
        self.assertFalse(BasicActions.exists(self.root, 'bar'))

    def test_remove_nonexistent(self):
        with self.assertRaises(NameError):
            BasicActions.remove(self.root, 'rabarbar')

    def test_remove_no_argument(self):
        with self.assertRaises(TypeError):
            BasicActions.remove(self.root)
        with self.assertRaises(TypeError):
            BasicActions.remove()


class CreateTests(ActionTests):
    def test_create_default_value(self):
        self.assertFalse(BasicActions.exists(self.root, 'rabarbar'))
        BasicActions.create(self.root, 'rabarbar')
        self.assertTrue(BasicActions.exists(self.root, 'rabarbar'))
        self.assertIsNone(BasicActions.get(self.root.get_node('rabarbar')))

    def test_create_specified_value(self):
        self.assertFalse(BasicActions.exists(self.root, 'rabarbar'))
        BasicActions.create(self.root, 'rabarbar', 12)
        self.assertTrue(BasicActions.exists(self.root, 'rabarbar'))
        self.assertEqual(12, BasicActions.get(self.root.get_node('rabarbar')))

    def test_create_existing(self):
        with self.assertRaises(NameError):
            BasicActions.create(self.root, 'foo')

    def test_create_no_argument(self):
        with self.assertRaises(TypeError):
            BasicActions.create(self.foo)
        with self.assertRaises(TypeError):
            BasicActions.create()

    def test_create_too_many_arguments(self):
        with self.assertRaises(TypeError):
            BasicActions.create(self.root, '.rabarbar', 'more', 'than', 1)

if __name__ == '__main__':
    unittest.main()
