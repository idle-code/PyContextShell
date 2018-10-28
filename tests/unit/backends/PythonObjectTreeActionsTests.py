import unittest
from abc import ABC, abstractmethod

from .bases import ActionTestsBase


class TestSubObject:
    field = 'SUB'


class TestRoot:
    field = 'text'

    def __init__(self):
        self.sub = TestSubObject()
        self._prop = 123

    @property
    def prop(self):
        return self._prop

    @prop.setter
    def prop(self, new_value):
        self._prop = new_value

    def method(self):
        pass


class PythonObjectTreeTestsBase(ActionTestsBase):
    def create_backend(self):
        from contextshell.backends.python import PythonObjectTree
        return PythonObjectTree(self.create_root_object())

    def create_root_object(self):
        return TestRoot()

    @property
    def root(self):
        return self.backend.root_object


class ContainsActionTests(PythonObjectTreeTestsBase):
    def test_nonexistent(self):
        obj_exists = self.execute('.', 'contains', 'nonexistent')

        self.assertFalse(obj_exists)

    def test_property(self):
        property_exists = self.execute('.', 'contains', 'prop')

        self.assertTrue(property_exists)

    def test_field(self):
        field_exists = self.execute('.', 'contains', 'field')

        self.assertTrue(field_exists)

    def test_protected(self):
        protected_exists = self.execute('.', 'contains', '_prop')

        self.assertFalse(protected_exists)

    def test_subobject_field(self):
        field_exists = self.execute('.sub', 'contains', 'field')

        self.assertTrue(field_exists)

    def test_method(self):
        method_exists = self.execute('.', 'contains', 'method')

        self.assertFalse(method_exists)


class GetActionTests(PythonObjectTreeTestsBase):
    def test_field(self):
        field_value = self.execute('.field', 'get')

        self.assertEqual(field_value, 'text')

    def test_property(self):
        property_value = self.execute('.prop', 'get')

        self.assertEqual(property_value, 123)

    def test_subobject_field(self):
        subobject_field_value = self.execute('.sub.field', 'get')

        self.assertEqual(subobject_field_value, 'SUB')


class SetActionTests(PythonObjectTreeTestsBase):
    def test_field(self):
        self.execute('.field', 'set', 'NEW')

        self.assertEqual(self.root.field, 'NEW')

    def test_property(self):
        self.execute('.prop', 'set', 'NEW')

        self.assertEqual(self.root.prop, 'NEW')


class ListActionTests(PythonObjectTreeTestsBase):
    def test_field(self):
        field_list = self.execute('.', 'list')

        self.assertIn('field', field_list)

    def test_property(self):
        field_list = self.execute('.', 'list')

        self.assertIn('prop', field_list)

    def test_subnode(self):
        field_list = self.execute('.', 'list')

        self.assertIn('sub', field_list)

    def test_method(self):
        field_list = self.execute('.', 'list')

        self.assertNotIn('method', field_list)


class ListActionsActionTests(PythonObjectTreeTestsBase):
    def test_field_have_set(self):
        field_actions = self.execute('.field', 'list.actions')

        self.assertIn('set', field_actions)


class ActionFromMethod(PythonObjectTreeTestsBase):
    def create_root_object(self):
        class ActionsFromMethodTestRoot:
            method_called = False

            def method(self):
                self.method_called = True

        return ActionsFromMethodTestRoot()

    def test_method_is_called(self):
        self.execute('.', 'method')

        self.assertTrue(self.root.method_called)
