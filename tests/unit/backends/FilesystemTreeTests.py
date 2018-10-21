import os
import tempfile
import unittest
from pathlib import Path
from typing import List

from contextshell.action import Executor

from .bases import Base

from contextshell.path import NodePath, NodePath as np  # isort:skip


def create_filesystem_tree(*args, **kwargs):
    from contextshell.backends.filesystem import FilesystemTree
    return FilesystemTree(*args, **kwargs)


class TemporaryDirectoryTestsBase(unittest.TestCase):
    """Test base for tests wishing to use actual filesystem directory"""
    def _make_test_path(self, relative_path):
        return Path(self.test_directory.name).joinpath(relative_path)

    def create_file(self, path: str, contents: str=''):
        with open(self._make_test_path(path), 'w') as file:
            file.write(contents)

    def create_directory(self, path):
        os.mkdir(self._make_test_path(path))

    def setUp(self):
        super().setUp()
        temp_dir_suffix = type(self).__name__
        self.test_directory = tempfile.TemporaryDirectory(temp_dir_suffix)

    def tearDown(self):
        self.test_directory.cleanup()
        super().tearDown()


class L0ActionsTests(TemporaryDirectoryTestsBase, Base.L0ActionsTests):
    def setUp(self):
        super().setUp()
        self.create_file('file')
        self.create_directory('directory')

    def create_backend(self) -> Executor:
        return create_filesystem_tree(self.test_directory.name)

    @property
    def existing_paths(self) -> List[NodePath]:
        return [np('file'), np('directory')]

    @property
    def nonexistent_paths(self) -> List[NodePath]:
        return [np('nonexistent')]
