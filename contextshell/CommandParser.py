from contextshell.Command import Command
from typing import List


def tokenize(text: str) -> List[str]:
    tokens = []
    tok = ''

    def end_token():
        nonlocal tok, tokens
        if len(tok) > 0:
            tokens.append(tok)
            tok = ''

    for char in text:
        if char in "{}:#":
            end_token()
            tokens.append(char)
        elif char.isspace():
            end_token()
        else:
            tok += char
    end_token()
    return tokens


class CommandParser:
    def __init__(self):
        self._root = None

    def parse(self, command_line: str) -> Command:
        tokens = tokenize(command_line)
        if len(tokens) == 0:
            return None  # ignore empty lines
        if tokens[0] == '#':
            return None  # ignore comments

        self._root = self._parse_scope(iter(tokens))
        return self._root

    def _parse_scope(self, token_iterator) -> Command:
        parts = []
        for tok in token_iterator:
            if tok == '{':
                parts.append(self._parse_scope(token_iterator))
            elif tok == '}':
                break
            else:
                parts.append(tok)

        if ':' in parts:
            cmd = Command(parts[2])
            cmd.target = parts[0]
            cmd.arguments = parts[3:]
            return cmd
        else:
            cmd = Command(parts[0])
            cmd.arguments = parts[1:]
            return cmd
