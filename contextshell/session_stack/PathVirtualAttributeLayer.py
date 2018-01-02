from contextshell.session_stack.VirtualAttributeLayerBase import VirtualAttributeLayerBase
from contextshell.session_stack.CrudSessionLayer import *


class PathVirtualAttributeLayer(VirtualAttributeLayerBase):
    """Layer providing @path attribute"""

    def __init__(self):
        super().__init__('path')

    def applies_to(self, path: NodePath) -> bool:
        return True

    def on_get(self, path: NodePath):
        return path
