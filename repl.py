#!/usr/bin/python3
from Tree import *
from Shell import *

import io
import readline

if __name__ == '__main__':
    tree = Tree()
    shell = Shell(tree)
    readline.parse_and_bind('tab: complete')
    #readline.set_completer(shell.completer_function)
    readline.set_completer_delims(' \t.')

    while True:
        try:
            command_line = input("{}: ".format(shell.current_path))
            command = shell.parse(command_line)
            result = tree.execute(command)
            if result != None:
                Shell.pretty_print(result)
        except EOFError: # exit on Ctrl+D
            break
        except Exception as ex:
            print("Error:", ex)


