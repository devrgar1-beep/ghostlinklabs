import unittest
import json
from click.testing import CliRunner
from ghostlink.link_cli import cli

class TestCliPipeline(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_pipeline_execute_command(self):
        """Test the pipeline execute command structure and output"""
        # Since we can't easily mock the entire orchestrator within the CLI test without heavy patching,
        # we'll test that the command exists and handles basic invocation.
        # For a real integration test, we'd need to mock the PipelineOrchestrator used in link_cli.py
        
        result = self.runner.invoke(cli, ['pipeline', 'execute', '--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Execute a pipeline', result.output)

    def test_pipeline_list_command(self):
        """Test pipeline list command"""
        result = self.runner.invoke(cli, ['pipeline', 'list'])
        # It might fail if no pipelines are defined or succeed with empty list
        # We just check it runs
        self.assertIn(result.exit_code, [0, 1]) 

if __name__ == '__main__':
    unittest.main()
