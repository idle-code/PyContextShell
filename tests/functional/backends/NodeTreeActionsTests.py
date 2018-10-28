import unittest

from tests.functional.bases import NodeTreeTestsBase
from tests.functional.TestExecutor import script_test


class CrudTestsBase(NodeTreeTestsBase):
    pass


class CreateTests(CrudTestsBase):
    @script_test
    def test_create(self):
        """
        $ .: create foo
        $ .: contains foo
        True
        """

    @script_test
    def test_create_many_parts(self):
        """
        $ .: create foo.bar
        $ .: contains foo.bar
        True
        """

    @unittest.skip("Check when type system will be working")
    @script_test
    def test_create_int_type(self):
        """
        $ .: create.int i 3
        $ .i: get
        3
        """


class ContainsTests(CrudTestsBase):
    @script_test
    def test_nonexistent(self):
        """
        $ .: contains unknown
        False
        """


class GetTests(CrudTestsBase):
    @script_test
    def test_get_existing(self):
        """
        $ .: create foo 1
        $ .foo: get
        1
        """

    @script_test
    def test_get_nonexistent(self):
        """
        $ .foo: get
        NameError: '.foo' doesn't exists
        """


class SetTests(CrudTestsBase):
    @script_test
    def test_set_existing(self):
        """
        $ .: create foo 1
        $ .foo: set 2
        $ .foo: get
        2
        """

    @script_test
    def test_set_nonexistent(self):
        """
        $ .foo: set 1
        NameError: '.foo' doesn't exists
        """

    @script_test
    def test_set_no_new_value(self):
        """
        $ .: create foo 1
        $ .foo: set
        TypeError: set_action() missing 1 required positional argument: 'new_value'
        """

    @script_test
    def test_set_different_type(self):
        """
        $ .: create foo 2
        $ .foo: set "rabarbar"
        TypeError: Cannot assign value with type 'str' to 'int' node
        """


class ListTests(CrudTestsBase):
    @script_test
    def test_list_empty(self):
        """
        $ .: create foo
        $ .foo: list
        """

    @script_test
    def test_list_in_creation_order(self):
        """
        $ .: create foo.Z_first
        $ .: create foo.A_second
        $ .foo: list
        Z_first
        A_second
        """

    @script_test
    def test_list_only_attributes(self):
        """
        $ .: create .test.@attr
        $ .: create .test.key
        $ .test: list.attributes
        @attr
        """

    @script_test
    def test_list_all(self):
        """
        $ .: create .test.@attr
        $ .: create .test.key
        $ .test: list.all
        @attr
        key
        """

    @script_test
    def test_list_only_normal(self):
        """
        $ .: create .test.@attr
        $ .: create .test.key
        $ .test: list
        key
        """

    @script_test
    def test_list_actions(self):
        """
        $ .: list.actions
        create
        contains
        get
        set
        list
        remove
        find
        """


class RemoveTests(CrudTestsBase):
    @script_test
    def test_remove_existing(self):
        """
        $ .: create foo
        $ .foo: remove
        $ .: contains foo
        False
        """

    @script_test
    def test_remove_nonexistent(self):
        """
        $ .foo: remove
        NameError: '.foo' doesn't exists
        """
