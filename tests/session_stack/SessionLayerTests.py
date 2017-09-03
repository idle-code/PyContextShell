import unittest
from contextshell.session_stack.SessionLayer import SessionLayer
from tests.session_stack.SessionLayerTestsBase import TestBases


class SessionLayerTests(TestBases.SessionLayerTestsBase):
    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        return SessionLayer()

if __name__ == '__main__':
    unittest.main()
