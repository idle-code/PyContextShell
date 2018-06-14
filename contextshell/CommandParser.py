from contextshell.Command import Command
from typing import List


def convert_token_type(token):
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        pass
    return token


def tokenize(text: str) -> List[str]:
    tokens = []
    tok = ''

    def finish_token():
        nonlocal tok, tokens
        if len(tok) > 0:
            tok = convert_token_type(tok)
            tokens.append(tok)
            tok = ''

    verbatim_mode = False
    verbatim_mode_finisher = None
    for char in text:
        if verbatim_mode:
            if char == verbatim_mode_finisher:
                finish_token()
                verbatim_mode = False
                verbatim_mode_finisher = None
            else:
                tok += char
        else:
            if char in "'\"":
                finish_token()
                verbatim_mode = True
                verbatim_mode_finisher = char
            elif char in "{}:#":
                finish_token()
                tokens.append(char)
            elif char.isspace():
                finish_token()
            else:
                tok += char
    finish_token()
    return tokens


class CommandParser:
    def __init__(self):
        self._root_scope = None

    def parse(self, command_line: str) -> Command:
        tokens = tokenize(command_line)
        if len(tokens) == 0:
            return None  # ignore empty lines
        if tokens[0] == '#':
            return None  # ignore comments

        self._root_scope = self._parse_scope(iter(tokens))
        return self._root_scope

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
