from abc import ABC, abstractmethod
from contextshell.NodePath import NodePath
from contextshell.TreeRoot import ActionArgsPack
from typing import Dict, Union, Any


class Action(ABC):
    def __init__(self, name: NodePath) -> None:
        assert isinstance(name, NodePath)
        assert name.is_relative
        self.name: NodePath = name

    @abstractmethod
    def invoke(self, target: NodePath, action: NodePath, arguments: ActionArgsPack):
        raise NotImplementedError()
