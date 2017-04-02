#!/usr/bin/python3
from TreeRoot import *
from Shell import *
import readline


if __name__ == '__main__':
    tree = TreeRoot()
    tree.create('test_node', "TODO")
    tree.create('tn', "2017-03-31")
    shell = Shell(tree)
    readline.parse_and_bind('tab: complete')
    #readline.set_completer(shell.completer_function)
    readline.set_completer_delims(' \t.')

    while True:
        try:
            command_line = input("{}: ".format(shell.current_path))
            result = shell.execute(command_line)
            if result is not None:
                Shell.pretty_print(result)
        except EOFError:  # exit on Ctrl+D
            break
        except Exception as ex:
            print("Error:", ex)
