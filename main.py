#!/usr/bin/python3
from ContextShell import *

import io
import readline


if __name__ == '__main__':
    shell = ContextShell(ContextNode('ContextShell 0.1'))
    readline.parse_and_bind('tab: complete')
    #readline.set_completer(shell.completer_function)
    readline.set_completer_delims(' \t.')

    while True:
        command_line = input("{}: ".format(shell.current_path))
        command = shell.parse(command_line)
        command.execute()

