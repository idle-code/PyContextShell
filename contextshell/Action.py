from abc import ABC, abstractmethod
from contextshell.NodePath import NodePath
from typing import Dict, Union, Any


class Action(ABC):
    def __init__(self, name: NodePath):
        assert name.is_relative
        self.name = name

    @abstractmethod
    def __call__(self, target: NodePath, action: NodePath, arguments: Dict[Union[NodePath, int], Any]):
        raise NotImplementedError()
