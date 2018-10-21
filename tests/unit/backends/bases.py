import unittest
from abc import ABC, abstractmethod
from typing import List

from contextshell.action import Executor, pack_argument_tree

from contextshell.path import NodePath, NodePath as np  # isort:skip


class Base:
    class ContainsActionTests(ABC, unittest.TestCase):
        @abstractmethod
        def create_backend(self) -> Executor:
            raise NotImplementedError()

        @property
        @abstractmethod
        def existing_paths(self) -> List[NodePath]:
            raise NotImplementedError()

        @property
        @abstractmethod
        def nonexistent_paths(self) -> List[NodePath]:
            raise NotImplementedError()

        def test_existing_paths(self):
            backend = self.create_backend()

            for path in self.existing_paths:
                with self.subTest("Existing path", path=path):
                    args = pack_argument_tree(path)
                    exists = backend.execute(np("."), np('contains'), args)
                    self.assertTrue(exists, f"{path} doesn't exist (but should)")

        def test_nonexistent_paths(self):
            backend = self.create_backend()

            for path in self.nonexistent_paths:
                with self.subTest("Nonexistent path", path=path):
                    args = pack_argument_tree(path)
                    exists = backend.execute(np("."), np('contains'), args)
                    self.assertFalse(exists, f"{path} exist (but shouldn't)")

    class L0ActionsTests(
        ContainsActionTests,
        ABC
    ):
        pass
