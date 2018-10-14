import unittest
import os
import tempfile
from pathlib import Path
from shutil import rmtree
from contextshell.backends.ActionExecutor import ActionExecutor
from contextshell.VirtualTree import VirtualTree
from tests.functional.ShellTestsBase import TreeRootTestsBase
from tests.functional.TestExecutor import script_test
from contextshell.backends.Filesystem import FilesystemRoot


class FilesystemTestsBase(TreeRootTestsBase):
    test_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')

    def create_tree_root(self) -> ActionExecutor:
        return FilesystemRoot(self.test_directory.name)

    def _make_test_path(self, relative_path):
        return Path(self.test_directory.name).joinpath(relative_path)

    def create_file(self, path: str, contents: str=''):
        with open(self._make_test_path(path), 'w') as file:
            file.write(contents)

    def create_directory(self, path):
        os.mkdir(self._make_test_path(path))

    def setUp(self):
        super().setUp()
        temp_dir_suffix = FilesystemTestsBase.__name__
        self.test_directory = tempfile.TemporaryDirectory(temp_dir_suffix)

    def tearDown(self):
        self.test_directory.cleanup()
        super().tearDown()


class FilesystemRootTests(FilesystemTestsBase):
    def setUp(self):
        super().setUp()
        self.create_file('test_file', "TEST_DATA")
        self.create_directory('dir')
        self.create_file('dir/nested')

    @script_test
    def test_contains_nonexistent_file(self):
        """
        $ .: contains nonexistent
        False
        """

    @script_test
    def test_contains_existing_file(self):
        """
        $ .: contains test_file
        True
        """

    @script_test
    def test_contains_existing_nested_file(self):
        """
        $ .dir: contains nested
        True
        """

    @script_test
    def test_get_contents(self):
        """
        $ .test_file: get
        TEST_DATA
        """

@unittest.skip("Those tests utilize attach actions which may not belong to the filesystem module")
class AttachTests(TreeRootTestsBase):
    def create_tree_root(self) -> ActionExecutor:
        pass

    def configure_virtual_tree(self, virtual_tree: VirtualTree):
        # TODO: install filesystem module/actions fot attaching
        # Note: VirtualTreeRoot *CAN* append data to the invoked commands
        # i.e. it can add attach.* commands to output of 'list.actions' (for completion)
        # TODO: find a (easy) way to support custom actions in VirtualTreeRoot
        pass

    @script_test
    def test_attach(self):
        """
        $ .: attach.filesystem .fs
        $ .: contains fs
        True
        """

    @script_test
    def test_detach(self):
        """
        $ .: attach.filesystem .fs
        $ .fs: detach
        $ .: contains fs
        False
        """


@unittest.skip("Re-enable when filesystem root is available")
class IsTests(FilesystemTestsBase):
    @script_test
    def test_contains_directory(self):
        """
        $ .: attach.filesystem .fs
        $ .fs: contains test_directory
        True
        """

    @script_test
    def test_contains_file(self):
        """
        $ .: attach.filesystem .fs
        $ .fs: contains test_file
        True
        """

    @script_test
    def test_is_directory(self):
        """
        $ .: attach.filesystem .fs
        $ .fs.test_directory: is.directory
        True
        $ .fs.test_directory: is.file
        False
        """

    @script_test
    def test_is_file(self):
        """
        $ .: attach.filesystem .fs
        $ .fs.test_file: is.directory
        False
        $ .fs.test_file: is.file
        True
        """
