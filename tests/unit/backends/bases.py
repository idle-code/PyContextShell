import unittest
from abc import ABC, abstractmethod
from typing import List

from contextshell.action import Executor, pack_argument_tree

from contextshell.path import NodePath, NodePath as np  # isort:skip


class ActionTestsBase(unittest.TestCase, ABC):
    @abstractmethod
    def create_backend(self):
        raise NotImplementedError()

    def setUp(self):
        super().setUp()
        self.backend = self.create_backend()

    def execute(self, target, action, *args, **kwargs):
        args_tree = pack_argument_tree(*args, **kwargs)
        return self.backend.execute(np(target), np(action), args_tree)
