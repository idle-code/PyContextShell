from contextshell.TreeRoot import TreeRoot, ActionArgsPack
from contextshell.NodePath import NodePath
from collections import OrderedDict


class VirtualTree(TreeRoot):
    def __init__(self):
        self.mounts: OrderedDict[NodePath, TreeRoot] = OrderedDict()

    def mount(self, path: NodePath, root: TreeRoot):
        if path.is_relative:
            raise ValueError("Could not mount relative path")
        if path in self.mounts:
            raise KeyError("Path '{}' is already provided by {}".format(path, self.mounts[path]))

        updated_items = list(self.mounts.items()) + [(path, root)]
        path_length_extractor = lambda pair: len(pair[0])
        self.mounts = OrderedDict(sorted(updated_items, key=path_length_extractor, reverse=True))

    def umount(self, path: NodePath):
        del self.mounts[path]

    def execute(self, target: NodePath, action: NodePath, args: ActionArgsPack=OrderedDict()):
        if target.is_relative:
            raise ValueError("Could not execute with relative target path")
        for path, root in self.mounts.items():
            if path.is_parent_of(target):
                remapped_target = target.relative_to(path)
                remapped_target.is_absolute = True
                return root.execute(remapped_target, action, args)
        else:
            raise RuntimeError("Could not find provider for path: '{}'".format(target))
