from typing import List

from contextshell.NodePath import NodePath
from contextshell.session_stack.CrudSessionLayer import CrudSessionLayer


class VirtualAttributeLayerBase(CrudSessionLayer):
    def __init__(self, name: str):
        super().__init__()
        self.attribute_name = '@' + name

    def on_get(self, path: NodePath):
        raise NotImplementedError()

    def set_value(self, path: NodePath, new_value):
        raise RuntimeError(self.attribute_name + " virtual attribute cannot be set")

    def applies_to(self, path: NodePath) -> bool:
        raise NotImplementedError()

    def get(self, path: NodePath):
        if path.base_name == self.attribute_name:
            if self.applies_to(path.base_path):
                return self.on_get(path.base_path)
        return self.next_layer.get(path)

    def set(self, path: NodePath, new_value):
        if path.base_name == self.attribute_name:
            if self.applies_to(path.base_path):
                return self.set_value(path.base_path, new_value)
        return self.next_layer.set(path, new_value)

    def exists(self, path: NodePath):
        if path.base_name == self.attribute_name:
            return self.applies_to(path.base_path)
        return self.next_layer.exists(path)

    def create(self, path: NodePath, value=None):
        if path.base_name == self.attribute_name:
            if self.applies_to(path.base_path):
                raise RuntimeError(self.attribute_name + " virtual attribute cannot be created")
        return self.next_layer.create(path, value)

    def remove(self, path: NodePath):
        if path.base_name == self.attribute_name:
            if self.applies_to(path.base_path):
                raise RuntimeError(self.attribute_name + " virtual attribute cannot be removed")
        return self.next_layer.remove(path)

    def list(self, path: NodePath) -> List[NodePath]:
        node_list = self.next_layer.list(path)
        if self.applies_to(path):
            node_list.append(NodePath.join(path, self.attribute_name))
        return node_list
