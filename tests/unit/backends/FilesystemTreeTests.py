import unittest

from contextshell.path import NodePath as np


def create_filesystem_tree(*args, **kwargs):
    from contextshell.backends.filesystem import FilesystemTree
    return FilesystemTree(*args, **kwargs)
