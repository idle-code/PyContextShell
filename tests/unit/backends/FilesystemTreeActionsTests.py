import os
import tempfile
import unittest
from pathlib import Path
from typing import List

from contextshell.action import Executor, pack_argument_tree

from .bases import Base

from contextshell.path import NodePath, NodePath as np  # isort:skip


def create_filesystem_tree(*args, **kwargs):
    from contextshell.backends.filesystem import FilesystemTree
    return FilesystemTree(*args, **kwargs)


class FilesystemTestsBase(unittest.TestCase):
    """Test base for tests wishing to use actual filesystem directory"""
    def _make_test_path(self, relative_path):
        return Path(self.test_directory.name).joinpath(relative_path)

    def create_file(self, path: str, contents: str=None):
        full_path = self._make_test_path(path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as file:
            file.write(contents if contents else '')

    def create_directory(self, path):
        os.mkdir(self._make_test_path(path))

    def setUp(self):
        super().setUp()
        temp_dir_suffix = type(self).__name__
        self.test_directory = tempfile.TemporaryDirectory(temp_dir_suffix)

    def tearDown(self):
        self.test_directory.cleanup()
        super().tearDown()


class ContainsActionTests(FilesystemTestsBase):
    @property
    def backend(self):
        return create_filesystem_tree(self.test_directory.name)

    def execute(self, target, action, *args, **kwargs):
        args_tree = pack_argument_tree(*args, **kwargs)
        return self.backend.execute(np(target), np(action), args_tree)

    def test_existing_file(self):
        self.create_file('file')

        exists = self.execute(".", "contains", 'file')

        self.assertTrue(exists)

    def test_existing_file_nested(self):
        self.create_file('parent/file')

        exists = self.execute(".", "contains", 'parent.file')

        self.assertTrue(exists)

    def test_existing_directory(self):
        self.create_directory('dir')

        exists = self.execute(".", "contains", 'dir')

        self.assertTrue(exists)

    def test_nonexistent(self):
        exists = self.execute(".", "contains", 'nonexistent')

        self.assertFalse(exists)

    def test_nonexistent_nested(self):
        self.create_directory('parent')

        exists = self.execute(".", "contains", 'parent.path')

        self.assertFalse(exists)
