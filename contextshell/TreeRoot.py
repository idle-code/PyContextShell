from abc import ABC, abstractmethod
from contextshell.NodePath import NodePath


class TreeRoot(ABC):
    @abstractmethod
    def execute(self, target: NodePath, action: NodePath, *args):  #FIXME: use Dict[Union[NodePath, int], Any] as arguments
        raise NotImplementedError()
