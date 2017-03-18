import unittest
from Command import Command


class CommandTests(unittest.TestCase):
    def test_initial_state(self):
        cmd = Command("init")
        self.assertEqual(None, cmd.target)
        self.assertEqual("init", cmd.name)
        self.assertListEqual([], cmd.arguments)

    def test_just_command_string(self):
        cmd = Command("foobar")
        self.assertEqual("foobar", str(cmd))

    def test_command_arguments_string(self):
        cmd = Command("foobar")
        cmd.arguments = ["foo", "bar", "spam"]
        self.assertEqual("foobar foo bar spam", str(cmd))

    def test_command_target_string(self):
        cmd = Command("foobar")
        cmd.target = "spam"
        self.assertEqual("spam: foobar", str(cmd))

    def test_nested_target_string(self):
        cmd = Command("foobar")
        cmd.target = Command("rabarbar")
        self.assertEqual("{rabarbar}: foobar", str(cmd))

    def test_nested_name_string(self):
        cmd = Command(Command("foobar"))
        cmd.target = "rabarbar"
        self.assertEqual("rabarbar: {foobar}", str(cmd))

    def test_nested_arguments_string(self):
        cmd = Command("foobar")
        cmd.arguments = [Command("spam"), Command("rabarbar")]
        self.assertEqual("foobar {spam} {rabarbar}", str(cmd))

if __name__ == '__main__':
    unittest.main()
