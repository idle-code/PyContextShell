from Command import Command


class CommandParser:
    def __init__(self):
        self.command_text = ""
        self._root = None

    @property
    def root(self):
        return self._root

    def parse(self, text: str) -> Command:
        cmd = Command(text)
        self._root = cmd
