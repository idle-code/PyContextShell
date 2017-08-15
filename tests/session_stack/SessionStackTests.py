import unittest

from contextshell.session_stack.SessionStack import *
from contextshell.SessionLayer import SessionLayer


class StorageLayerMock(SessionLayer):
    def __init__(self):
        self.was_started = False
        self.was_finished = False

    def start(self):
        self.was_started = True

    def finish(self):
        self.was_finished = True


class SessionStackTests(unittest.TestCase):
    def setUp(self):
        self.storage_layer = StorageLayerMock()
        #self.stack = SessionStack(self.storage_layer)

    def test_push(self):
        pass


if __name__ == '__main__':
    unittest.main()
