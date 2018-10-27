import unittest
from abc import ABC, abstractmethod

from .bases import ActionTestsBase


class PythonObjectTreeTestsBase(ActionTestsBase, ABC):
    def create_backend(self):
        from contextshell.backends.python import PythonObjectTree
        return PythonObjectTree(self.create_root_object())

    @abstractmethod
    def create_root_object(self):
        raise NotImplementedError()


class ContainsActionTests(PythonObjectTreeTestsBase):
    def create_root_object(self):
        class TestRoot:
            field = 'text'

            @property
            def prop(self):
                return 123

            def method(self):
                pass

        return TestRoot()

    def test_nonexistent(self):
        obj_exists = self.execute('.', 'contains', 'nonexistent')

        self.assertFalse(obj_exists)

    def test_property(self):
        property_exists = self.execute('.', 'contains', 'prop')

        self.assertTrue(property_exists)

    def test_field(self):
        field_exists = self.execute('.', 'contains', 'field')

        self.assertTrue(field_exists)

    def test_method(self):
        method_exists = self.execute('.', 'contains', 'method')

        self.assertFalse(method_exists)
