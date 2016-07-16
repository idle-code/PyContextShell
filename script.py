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
            if len(line) == 0:
                continue # ignore empty lines
            if line.startswith('#'):
                print(line) # print comments
                continue
            print("COMMAND:", line)
            command = shell.parse(line)
            result = tree.execute(command)
            if result != None:
                if isinstance(result, list):
                    for r in result:
                        print("{}\t = {}".format(r["@name"], r))
                else: # print scalar
                    print(result)

