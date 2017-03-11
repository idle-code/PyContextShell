#!/usr/bin/python3
from Tree import *
from Shell import *

import io
import sys

if len(sys.argv) < 2:
    raise ValueError('Script requires single argument')

tree = Tree()
shell = Shell(tree)

with open(sys.argv[1]) as script:
    for line in script.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith('#'):
            print(line)
            continue

        print("$", line)
        command = shell.parse(line)
        if command is None:
            print("WARNING: No parse output for: '{}'".format(line))
            continue

        result = tree.execute(command)
        if result is not None:
            Shell.pretty_print(result)

