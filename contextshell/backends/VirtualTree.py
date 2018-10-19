from collections import OrderedDict
from typing import Dict

from ..action import Executor, ActionArgsPack
from ..path import NodePath


class VirtualTree(Executor):
    """Abstract frontend allowing embedding (mounting) of more specific tree roots"""

    def __init__(self):
        self.mounts: Dict[NodePath, Executor] = OrderedDict()

    # TODO: rename to attach/detach
    def mount(self, path: NodePath, root: Executor):
        if path.is_relative:
            raise ValueError("Could not mount relative path")
        if path in self.mounts:
            raise KeyError("Path '{}' is already provided by {}".format(path, self.mounts[path]))

        def path_length_extractor(path_root_pair):
            return len(path_root_pair[0])

        # CHECK: use bisect module for maintaining mount point list?
        updated_items = list(self.mounts.items()) + [(path, root)]
        self.mounts = OrderedDict(sorted(updated_items, key=path_length_extractor, reverse=True))

    def umount(self, path: NodePath):
        del self.mounts[path]

    def execute(self, target: NodePath, action_name: NodePath, args: ActionArgsPack = None):
        if target.is_relative:
            raise ValueError("Could not invoke action with relative target path")
        if not args:
            args = OrderedDict()
        for path, root in self.mounts.items():
            if path.is_parent_of(target):
                remapped_target = target.relative_to(path)
                remapped_target.is_absolute = True
                return root.execute(remapped_target, action_name, args)
        raise RuntimeError("Could not find provider for path: '{}'".format(target))
