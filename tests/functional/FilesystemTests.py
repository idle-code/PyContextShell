import unittest
import os
import tempfile
from contextshell.TreeRoot import TreeRoot
from contextshell.VirtualTree import VirtualTree
from tests.functional.ShellTestsBase import TreeRootTestsBase
from tests.functional.TestExecutor import script_test
from contextshell.backends.Filesystem import FilesystemRoot


class FilesystemTestsBase(TreeRootTestsBase):
    test_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')

    def create_tree_root(self) -> TreeRoot:
        self.test_directory = tempfile.TemporaryDirectory(FilesystemTestsBase.__name__)
        return FilesystemRoot(self.test_directory.name) # FIXME: make this work

    def setUp(self):
        super().setUp()
        # TODO: create test directory

    def tearDown(self):
        # TODO: remove test directory
        super().tearDown()


class FilesystemRootTests(FilesystemTestsBase):
    def setUp(self):
        super().setUp()
        # TODO: populate test directory

    @script_test
    def test_contains_existing_file(self):
        """
        $ .: contains test_file
        True
        """


@unittest.skip("Those tests utilize attach actions which may not belong to the filesystem module")
class AttachTests(TreeRootTestsBase):
    def create_tree_root(self) -> TreeRoot:
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
