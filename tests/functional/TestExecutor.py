from typing import List, Tuple


class TestExecutor:
    def __init__(self, shell):
        self.shell = shell

    def test(self, test_script: str):
        for command, expected_output in self._parse_script(test_script):
            output = self.shell.execute(command)
            if expected_output != output:
                raise AssertionError("""
Command: {command}
Expected output:
  {expected}
Actual output:
  {actual}""".format(
                    command=repr(command),
                    actual=repr(output),
                    expected=repr(expected_output)))

    def _parse_script(self, script_text: str) -> List[Tuple[str, str]]:
        commands = []
        script_text = script_text.strip()
        script_lines = list(map(str.strip, script_text.split('\n')))
        i = 0
        while i < len(script_lines):
            line = script_lines[i]
            if not line.startswith('$'):
                raise ValueError("Expected command but got output in tests script")
            command = line[1:].strip()
            i += 1

            output_lines = []
            while i < len(script_lines):
                line = script_lines[i]
                if line.startswith('$'):
                    break
                output_lines.append(line)
                i += 1

            if len(output_lines) > 0:
                expected_output = "\n".join(output_lines)
            else:
                expected_output = None

            commands.append((command, expected_output))

        return commands


def script_test(method):
    def executor(self):
        shell = self.create_shell()
        exec = TestExecutor(shell)
        test_script = method.__doc__
        exec.test(test_script)
    return executor
