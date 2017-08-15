#!/usr/bin/python3
import sys

from TreeRoot import *

from contextshell.Shell import *

if len(sys.argv) < 2:
    raise ValueError('Script requires single argument')

tree = TreeRoot()
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
        result = shell.execute(line)
        if result is not None:
            Shell.pretty_print(result)
