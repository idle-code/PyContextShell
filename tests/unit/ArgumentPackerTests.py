import unittest
from contextshell.TreeRoot import pack_argument_tree, unpack_argument_tree, parse_argument_tree
from contextshell.NodePath import NodePath as np
from collections import OrderedDict


class UnpackArgumentTreeTests(unittest.TestCase):
    def test_unpack_ordered(self):
        packed = OrderedDict([
            (0, 'foo'),
            (1, 'bar'),
        ])

        args, _ = unpack_argument_tree(packed)

        self.assertSequenceEqual(['foo', 'bar'], args)

    def test_unpack_mixed_order(self):
        packed = OrderedDict([
            (1, 'bar'),
            (0, 'foo'),
        ])

        args, _ = unpack_argument_tree(packed)

        self.assertSequenceEqual(['foo', 'bar'], args)

    def test_unpack_invalid_index(self):
        packed = OrderedDict([
            (1, 'bar'),
        ])

        with self.assertRaises(AssertionError):
            unpack_argument_tree(packed)

    def test_unpack_keyed(self):
        packed = OrderedDict([
            (np('foo'), 1),
            (np('bar'), 2),
        ])

        _, kwargs = unpack_argument_tree(packed)

        self.assertDictEqual({
            np('foo'): 1,
            np('bar'): 2,
        }, kwargs)

    def test_unpack_mixed(self):
        packed = OrderedDict([
            (np('foo'), 1),
            (1, 'bar'),
        ])

        args, kwargs = unpack_argument_tree(packed)

        self.assertSequenceEqual(['bar'], args)
        self.assertDictEqual({
            np('foo'): 1,
        }, kwargs)

    def test_unpack_path_to_python_name(self):
        packed = OrderedDict([
            (np('foo.bar'), 1)
        ])

        _, kwargs = unpack_argument_tree(packed)
        self.assertDictEqual({
            'foo_bar': 1,
        }, kwargs)


class PackArgumentTreeTests(unittest.TestCase):
    def test_pack_ordered(self):
        args = ['foo', 'bar']
        kwargs = {}

        packed = pack_argument_tree(*args, **kwargs)

        self.assertEqual(OrderedDict([
            (0, 'foo'),
            (1, 'bar')
        ]), packed)

    def test_pack_keyed(self):
        args = []
        kwargs = {
            'foo': 2,
            'bar': 1
        }

        packed = pack_argument_tree(*args, **kwargs)

        self.assertDictEqual({
            np('bar'): 1,
            np('foo'): 2
        }, packed)

    def test_key_is_converted_to_path(self):
        args = []
        kwargs = {
            'foo_bar': 1,
        }

        packed = pack_argument_tree(*args, **kwargs)

        self.assertDictEqual({
            np('foo.bar'): 1
        }, packed)


class ParseArgumentTreeTests(unittest.TestCase):
    def test_parse_empty(self):
        args = []

        packed = parse_argument_tree(args)

        self.assertEqual(0, len(packed))

    def test_parse_positional(self):
        args = ['foo', 'bar']

        packed = parse_argument_tree(args)

        self.assertEqual(OrderedDict([
            (0, 'foo'),
            (1, 'bar'),
        ]), packed)

    def test_parse_keyword_string(self):
        args = ['foo=rabarbar']

        packed = parse_argument_tree(args)

        self.assertEqual(OrderedDict([
            (np('foo'), 'rabarbar'),
        ]), packed)

    def test_parse_keyword_int(self):
        args = ['foo=3']

        packed = parse_argument_tree(args)

        self.assertEqual(OrderedDict([
            (np('foo'), 3),
        ]), packed)

    def test_parse_keyword_path(self):
        args = ['foo.bar=spam']

        packed = parse_argument_tree(args)

        self.assertEqual(OrderedDict([
            (np('foo.bar'), 'spam'),
        ]), packed)

    def test_parse_absolute_path_raises(self):
        args = ['.foo=spam']

        with self.assertRaises(ValueError):
            parse_argument_tree(args)
