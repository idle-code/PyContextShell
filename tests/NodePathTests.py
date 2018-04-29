import unittest
from contextshell.NodePath import *


def create_path(representation: str) -> NodePath:
    """Creates instance of NodePath from provided representation"""
    return NodePath(representation)


class JoinTests(unittest.TestCase):
    def test_join_two_absolute_paths(self):
        foo = NodePath('.foo')
        bar = NodePath('.bar')

        joined_path = NodePath.join(foo, bar)

        self.assertEqual(joined_path, create_path('.foo.bar'))

    def test_join_list(self):
        # CHECK: is this used anywhere?
        rabarbar = NodePath.join('ra', 'bar', 'bar')

        self.assertEqual(rabarbar, NodePath(['ra', 'bar', 'bar']))


class CastTests(unittest.TestCase):
    def test_cast_none(self):
        none_path = NodePath.cast(None)

        self.assertEqual(none_path, create_path(''))

    def test_cast_representation(self):
        name_path = NodePath.cast('foo.bar')

        self.assertEqual(name_path, create_path('foo.bar'))


class StringParsingConstructorTests(unittest.TestCase):
    def test_constructor_from_string_matches_length(self):
        relative_path = NodePath('a.b.c')

        self.assertEqual(3, len(relative_path))

    def test_constructor_from_string_trailing_separator(self):
        relative_path = NodePath('a.b.c.')

        self.assertEqual(3, len(relative_path))

    def test_constructor_from_relative_string(self):
        relative_path = NodePath('a.b.c')

        relative_path_is_absolute = relative_path.is_absolute

        self.assertFalse(relative_path_is_absolute)

    def test_constructor_from_index_string(self):
        index_path = NodePath('1.2.3')

        self.assertEqual(3, len(index_path))

    def test_constructor_from_absolute_string(self):
        absolute_path = NodePath('.a.b.c')

        absolute_path_is_absolute = absolute_path.is_absolute

        self.assertTrue(absolute_path_is_absolute)

    def test_constructor_from_index_string_preserve_element_type(self):
        index_path = NodePath('1.2.3')

        element = index_path[0]

        self.assertEqual(type(element), type(1))


class ConstructorTests(unittest.TestCase):
    def test_default_constructor_creates_empty_path(self):
        empty = NodePath()

        self.assertEqual(0, len(empty))

    def test_default_constructor_creates_relative_path(self):
        empty = NodePath()

        empty_is_absolute = empty.is_absolute

        self.assertFalse(empty_is_absolute)

    def test_constructor_from_single_index(self):
        index_path = NodePath(3)

        self.assertEqual(1, len(index_path))

    def test_constructor_from_list_creates_relative_path(self):
        path = NodePath(['a', 'b', 'c'])

        path_is_absolute = path.is_absolute

        self.assertFalse(path_is_absolute)

    def test_constructor_from_list(self):
        path = NodePath(['a', 'b', 'c'])

        self.assertEqual(3, len(path))

    def test_constructor_from_index_list(self):
        index_path = NodePath([1, 2, 3])

        self.assertEqual(3, len(index_path))

    def test_constructor_from_index_list_is_relative(self):
        index_path = NodePath([1])

        index_path_is_absolute = index_path.is_absolute

        self.assertFalse(index_path_is_absolute)

    def test_constructor_from_index_list_preserve_element_type(self):
        # CHECK: is this test really needed?
        index_path = NodePath([1])

        element = index_path[0]

        self.assertEqual(type(element), type(1))

    def test_constructor_from_existing_instance(self):
        path = create_path('foo.bar')

        path_copy = NodePath(path)

        self.assertEqual(path, path_copy)

    def test_constructor_from_float_throws(self):
        with self.assertRaises(ValueError):
            NodePath(3.13)


class BasePathTests(unittest.TestCase):
    def test_basepath_skips_last_element(self):
        path = create_path('foo.bar.spam')

        base_path = path.base_path

        self.assertEqual(base_path, create_path('foo.bar'))

    def test_basepath_of_relative_is_relative(self):
        path = create_path('foo.bar.spam')

        base_path = path.base_path

        self.assertFalse(base_path.is_absolute)

    def test_basepath_of_absolute_is_absolute(self):
        path = create_path('.foo.bar.spam')

        base_path = path.base_path

        self.assertTrue(base_path.is_absolute)


class BaseNameTests(unittest.TestCase):
    def test_basename(self):
        path = create_path('foo.bar')

        path_base_name = path.base_name

        self.assertEqual(path_base_name, 'bar')

    def test_basename_from_empty(self):
        path = create_path('')

        path_base_name = path.base_name

        self.assertIsNone(path_base_name)


class IsParentOfTests(unittest.TestCase):
    def test_is_parent_of(self):
        foo = NodePath.cast('.foo')
        foobar = NodePath.cast('.foo.bar')
        self.assertTrue(foo.is_parent_of(foobar))
        self.assertFalse(foobar.is_parent_of(foo))

    def test_longer_is_parent_of_shorter(self):
        longer = create_path('foo.bar')
        shorter = create_path('foo')

        longer_is_parent_of_shorter = longer.is_parent_of(shorter)

        self.assertFalse(longer_is_parent_of_shorter)

    def test_is_parent_of_same_length(self):
        foobar1 = create_path('foo.bar')
        foobar2 = create_path('foo.bar')

        foobar_is_parent_of_foobar = foobar1.is_parent_of(foobar2)

        self.assertTrue(foobar_is_parent_of_foobar)

    def test_relative_is_parent_of_relative(self):
        foo = create_path('foo')
        foobar = create_path('foo.bar')

        foo_is_parent_of_foobar = foo.is_parent_of(foobar)

        self.assertTrue(foo_is_parent_of_foobar)

    def test_absolute_is_parent_of_absolute(self):
        foo = create_path('.foo')
        foobar = create_path('.foo.bar')

        foo_is_parent_of_foobar = foo.is_parent_of(foobar)

        self.assertTrue(foo_is_parent_of_foobar)

    def test_relative_is_parent_of_absolute(self):
        foo = create_path('foo')
        foobar = create_path('.foo.bar')

        with self.assertRaises(ValueError):
            foo.is_parent_of(foobar)

    def test_absolute_is_parent_of_relative(self):
        foo = create_path('.foo')
        foobar = create_path('foo.bar')

        with self.assertRaises(ValueError):
            foo.is_parent_of(foobar)


class RelativeToTests(unittest.TestCase):
    def test_relative_to(self):
        foo = create_path('.foo')
        foobar = create_path('.foo.bar')

        foobar_relative_to_foo = foobar.relative_to(foo)

        self.assertEqual(foobar_relative_to_foo, create_path('bar'))

    def test_relative_to_no_common_base(self):
        foobar = create_path('.foo.bar')
        spamrabbit = create_path('.spam.rabbit')

        with self.assertRaises(ValueError):
            foobar.relative_to(spamrabbit)

    def test_absolute_relative_to_relative(self):
        absolute = create_path('.foo.bar')
        relative = create_path('foo')

        with self.assertRaises(ValueError):
            absolute.relative_to(relative)

    def test_relative_relative_to_absolute(self):
        relative = create_path('foo.bar')
        absolute = create_path('.foo')

        with self.assertRaises(ValueError):
            relative.relative_to(absolute)


class EqualOperatorTests(unittest.TestCase):
    def test_compare_same(self):
        foo1 = create_path('foo')
        foo2 = create_path('foo')

        are_equal = foo1 == foo2

        self.assertTrue(are_equal)

    def test_compare_different(self):
        foo = create_path('foo')
        bar = create_path('bar')

        are_equal = foo == bar

        self.assertFalse(are_equal)

    def test_compare_absolute_relative(self):
        absolute_foo = create_path('.foo')
        relative_foo = create_path('foo')

        are_equal = absolute_foo == relative_foo

        self.assertFalse(are_equal)

    def test_differ_same(self):
        foo1 = create_path('foo')
        foo2 = create_path('foo')

        are_not_equal = foo1 != foo2

        self.assertFalse(are_not_equal)

    def test_differ_different(self):
        foo = create_path('foo')
        bar = create_path('bar')

        are_not_equal = foo != bar

        self.assertTrue(are_not_equal)


if __name__ == '__main__':
    unittest.main()
