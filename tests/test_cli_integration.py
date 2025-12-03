import unittest

from click.testing import CliRunner

from ghostlink.link_cli import cli


class TestCliIntegration(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_audit_run_cli(self):
        result = self.runner.invoke(cli, ["audit", "run"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Audit complete", result.output)

    def test_health_check_cli(self):
        result = self.runner.invoke(cli, ["health", "check"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Health check complete", result.output)


if __name__ == "__main__":
    unittest.main()
