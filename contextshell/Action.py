from abc import ABC, abstractmethod
from contextshell.NodePath import NodePath
from typing import Dict, Union, Any


class Action(ABC):
    def __init__(self, name: NodePath):
        assert isinstance(name, NodePath)
        assert name.is_relative
        self.name: NodePath = name

    @abstractmethod
    def invoke(self, target: NodePath, action: NodePath, arguments: Dict[Union[NodePath, int], Any]):
        raise NotImplementedError()
