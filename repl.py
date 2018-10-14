#!/usr/bin/python3.6
import readline

from contextshell.TreeRoot import *
from contextshell.Shell import *

def create_context_tree() -> TreeRoot:
    pass

if __name__ == '__main__':
    tree = create_context_tree()
    session = tree.create_session()
    session.create('test_node', "TODO")
    session.create('tn', "2017-03-31")
    shell = Shell(session)
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

