from tests.integration.ScriptTestBase import ScriptTestBase, script_test


class CrudTests(ScriptTestBase):
    @script_test
    def test_get(self):
        """
        > .: create foo 1
        > .foo: get
        1
        """
