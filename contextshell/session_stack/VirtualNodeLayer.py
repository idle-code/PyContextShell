from contextshell.session_stack.SessionLayer import *
from typing import List


class VirtualNodeLayer(SessionLayer):
    """Layer allowing easy creation of virtual nodes"""

    def __init__(self, virtual_path: NodePath):
        super().__init__()
        self.virtual_path = virtual_path
