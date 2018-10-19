import os
import tempfile
from pathlib import Path
from contextshell.action import ActionExecutor
from tests.functional.ShellTestsBase import TreeRootTestsBase
from tests.functional.TestExecutor import script_test
from contextshell.backends.FilesystemTree import FilesystemTree


class FilesystemTestsBase(TreeRootTestsBase):
    test_directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')

    def create_tree_root(self) -> ActionExecutor:
        return FilesystemTree(self.test_directory.name)

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


class ContainsTests(FilesystemTestsBase):
    def setUp(self):
        super().setUp()
        self.create_file('test_file')
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
    def test_contains_existing_directory(self):
        """
        $ .: contains dir
        True
        """

    @script_test
    def test_contains_existing_nested_file(self):
        """
        $ .dir: contains nested
        True
        """

    @script_test
    def test_contains_existing_nested_argument(self):
        """
        $ .: contains dir.nested
        True
        """


class GetTests(FilesystemTestsBase):
    def setUp(self):
        super().setUp()
        self.create_file('file', "TEST_DATA")
        self.create_directory('dir')

    @script_test
    def test_get_file_contents(self):
        """
        $ .file: get
        TEST_DATA
        """

    @script_test
    def test_get_directory_contents(self):
        """
        $ .dir: get
        """


class SetTests(FilesystemTestsBase):
    def setUp(self):
        super().setUp()
        self.create_file('file', "TEST_DATA")
        self.create_directory('dir')

    # TODO: implement


class ListTests(FilesystemTestsBase):
    def setUp(self):
        super().setUp()
        self.create_directory('empty')
        self.create_file('file')
        self.create_directory('dir')
        self.create_file('dir/nested')

    @script_test
    def test_empty(self):
        """
        $ .empty: list
        """

    @script_test
    def test_nested(self):
        """
        $ .dir: list
        nested
        """

    @script_test
    def test_sorted_order(self):
        """
        $ .: list
        dir
        empty
        file
        """

    @script_test
    def test_nested(self):
        """
        $ .dir: list
        nested
        """

    @script_test
    def test_file(self):
        """
        $ .file: list
        """

    @script_test
    def test_actions(self):
        # CHECK: should multipart actions be listed?
        # CHECK: what if first part of multipart action is not executable (e.g 'is' in is.file)?
        """
        $ .: list.actions
        contains
        get
        is.file
        is.directory
        list
        list.actions
        """


class IsTests(FilesystemTestsBase):
    def setUp(self):
        super().setUp()
        self.create_file('file')
        self.create_directory('dir')

    @script_test
    def test_is_file_existing_file(self):
        """
        $ .file: is.file
        True
        """

    @script_test
    def test_is_file_existing_directory(self):
        """
        $ .dir: is.file
        False
        """

    @script_test
    def test_is_directory_existing_file(self):
        """
        $ .file: is.directory
        False
        """

    @script_test
    def test_is_file_existing_directory(self):
        """
        $ .dir: is.directory
        True
        """
