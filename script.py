#!/usr/bin/python3
from ContextTree import *
from ContextShell import *

import io
import sys

if __name__ == '__main__':
    tree = ContextTree()
    shell = ContextShell(tree)

    with open(sys.argv[1]) as script:
        for line in script.readlines():
            line = line.strip()
            print("COMMAND:", line)
            command = shell.parse(line)
            result = tree.execute(command)
            print("RESULT:", result)

