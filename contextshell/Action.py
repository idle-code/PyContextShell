from abc import ABC, abstractmethod
from contextshell.NodePath import NodePath
from typing import Dict, Union, Any


class Action(ABC):
    @abstractmethod
    def __call__(self, target: NodePath, action: NodePath, arguments: Dict[Union[NodePath, int], Any]):
        raise NotImplementedError()
