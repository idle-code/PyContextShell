#!/usr/bin/python3
from ContextTree import *
from ContextShell import *

import io
import readline

if __name__ == '__main__':
    tree = ContextTree()
    shell = ContextShell(tree)
    readline.parse_and_bind('tab: complete')
    #readline.set_completer(shell.completer_function)
    readline.set_completer_delims(' \t.')

    while True:
        command_line = input("{}: ".format(shell.current_path))
        command = shell.parse(command_line)
        tree.execute(command)
        #try:
        #    command = shell.parse(command_line)
        #    command.invoke()
        #except Exception as ex:
        #    print("Error:", ex)


