
class Command:
    """Represents single command line typed in the shell"""

    def __init__(self, command_name):
        self.target = None
        self.name = command_name
        self.arguments = []

    def __str__(self):
        cmd_invocation = " ".join(map(Command._to_string, [self.name] + self.arguments))
        if self.target is None:
            return cmd_invocation
        return "{}: {}".format(Command._to_string(self.target), cmd_invocation)

    @staticmethod
    def _to_string(param):
        if isinstance(param, Command):
            return "{{{}}}".format(str(param))
        return str(param)
