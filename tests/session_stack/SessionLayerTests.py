import unittest
from unittest.mock import MagicMock
from contextshell.session_stack.CrudSessionLayer import CrudSessionLayer
from tests.session_stack.TestBases import TestBases


class SessionLayerTests(TestBases.SessionLayerTestsBase):
    def prepare_layer(self, session: CrudSessionLayer) -> CrudSessionLayer:
        return CrudSessionLayer()


class CrudSessionLayerTests(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
