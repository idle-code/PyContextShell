import unittest

from contextshell.session_stack.VirtualNodeLayer import *
from contextshell.session_stack.SessionStack import *
from contextshell.TreeRoot import TreeRoot


class TestedVirtualNodeLayer(VirtualNodeLayer):
    pass


class VirtualMappingLayerTests(unittest.TestCase):
    def setUp(self):
        self.virtual_path = NodePath('.virtual')
        self.foo_path = NodePath('.foo')

        root = TreeRoot()
        # Create backing and test nodes
        session = root.create_session()

        # Setup session stack (to push TemporarySession on top)
        self.storage_layer = root.create_session()
        session_stack = SessionStack(self.storage_layer)
        session_stack.push(TestedVirtualNodeLayer(self.virtual_path))
        self.session = session_stack



if __name__ == '__main__':
    unittest.main()
