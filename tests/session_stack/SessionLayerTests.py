import unittest
from SessionLayerTestsBase import *


class SessionLayerTests(TestBases.SessionLayerTestsBase):
    def prepare_layer(self, session: SessionLayer) -> SessionLayer:
        return SessionLayer()
