from NodePath import *

import unittest

class NodePathTests(unittest.TestCase):
    def test_empty(self):
        empty = NodePath()
        self.assertEqual(0, len(empty))
        self.assertFalse(empty.isabsolute)

    def test_constructor(self):
        l = NodePath(['a', 'b', 'c'])
        self.assertEqual(3, len(l))
        self.assertFalse(l.isabsolute)
        self.assertEqual('a.b.c', str(l))

    def test_parse(self):
        p = NodePath('a.b.c')
        self.assertEqual(3, len(p))
        self.assertFalse(p.isabsolute)
        self.assertEqual('a.b.c', str(p))

        pa = NodePath('.a.b.c')
        self.assertEqual(3, len(pa))
        self.assertTrue(pa.isabsolute)
        self.assertEqual('.a.b.c', str(pa))

    def test_basename(self):
        abc = NodePath('a.b.c')
        self.assertEqual(3, len(abc))
        self.assertFalse(abc.isabsolute)
        self.assertEqual('c', abc.base_name)

        base_path = abc.base_path
        self.assertEqual(2, len(base_path))
        self.assertFalse(base_path.isabsolute)
        self.assertEqual('a.b', str(base_path))
        self.assertEqual('b', base_path.base_name)

    def test_index(self):
        ab2c = NodePath(['a', 'b', 2, 'c'])

        self.assertEqual(4, len(ab2c))
        self.assertEqual('a.b.2.c', str(ab2c))

    def test_index_parse(self):
        ab2c = NodePath('.a.b.2.c')

        self.assertEqual(4, len(ab2c))
        self.assertEqual('.a.b.2.c', str(ab2c))

if __name__ == '__main__':
    unittest.main()

