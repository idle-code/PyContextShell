from contextshell.NodeTreeRoot import NodeTreeRoot
from contextshell.NodePath import NodePath
from functional.ShellTestsBase import NodeTreeTestsBase
from tests.functional.TestExecutor import script_test
import unittest


class CrudTestsBase(NodeTreeTestsBase):
    pass


class CreateTests(CrudTestsBase):
    @script_test
    def test_create(self):
        """
        > .: create foo
        > .: exists foo
        True
        """

    @script_test
    def test_create_many_parts(self):
        """
        > .: create foo.bar
        > .: exists foo.bar
        True
        """


class ExistsTests(CrudTestsBase):
    @script_test
    def test_exists_nonexistent(self):
        """
        > .: exists unknown
        False
        """


class GetTests(CrudTestsBase):
    @script_test
    def test_get_existing(self):
        """
        > .: create foo 1
        > .foo: get
        1
        """

    @script_test
    def test_get_nonexistent(self):
        """
        > .foo: get
        NameError: '.foo' doesn't exists
        """


class SetTests(CrudTestsBase):
    @script_test
    def test_set_existing(self):
        """
        > .: create foo 1
        > .foo: set 2
        > .foo: get
        2
        """

    @script_test
    def test_set_nonexistent(self):
        """
        > .foo: set 1
        NameError: '.foo' doesn't exists
        """

    @script_test
    def test_set_no_new_value(self):
        """
        > .: create foo 1
        > .foo: set
        TypeError: set_action() missing 1 required positional argument: 'new_value'
        """

    @script_test
    def test_set_different_type(self):
        """
        > .: create foo 2
        > .foo: set "rabarbar"
        TypeError: Cannot assign value with type 'str' to 'int' node
        """


class ListTests(CrudTestsBase):
    def install_custom_actions(self, finder):
        super().install_custom_actions(finder)

        def list_actions(tree: NodeTreeRoot, target: NodePath, action: NodePath):
            from contextshell.ActionFinder import ActionFinder
            actions_branch = NodePath.join(target, ActionFinder.actions_branch_name)
            return tree.list(actions_branch)

        finder.install_action(".", "list.actions", list_actions)

    @script_test
    def test_list_empty(self):
        """
        > .: create foo
        > .foo: list
        """

    @script_test
    def test_list_action(self):
        """
        > .: list.actions
        exists
        create
        get
        set
        list
        remove
        """

    @script_test
    def test_list_in_creation_order(self):
        """
        > .: create foo.Z_first
        > .: create foo.A_second
        > .foo: list
        Z_first
        A_second
        """
    # TODO: list.attributes
    # TODO: list.all


class RemoveTests(CrudTestsBase):
    @script_test
    def test_remove_existing(self):
        """
        > .: create foo
        > .foo: remove
        > .: exists foo
        False
        """

    @script_test
    def test_remove_nonexistent(self):
        """
        > .foo: remove
        NameError: '.foo' doesn't exists
        """
