import asyncio
import unittest
from unittest.mock import Mock

from ghostlink.orchestrator import PipelineOrchestrator, PipelineStatus, TaskStatus


class TestOrchestratorRetries(unittest.TestCase):
    def setUp(self):
        self.orchestrator = PipelineOrchestrator("test_retry_pipeline")

    def test_task_retry_success(self):
        """Test that a task retries and eventually succeeds"""

        # Create a mock handler that fails twice then succeeds
        mock_handler = Mock(side_effect=[Exception("Fail 1"), Exception("Fail 2"), "Success"])

        async def async_handler():
            return mock_handler()

        self.orchestrator.add_task(name="retry_task", handler=async_handler, max_retries=3)

        asyncio.run(self.orchestrator.execute())

        task = self.orchestrator.tasks["retry_task"]
        self.assertEqual(task.status, TaskStatus.SUCCESS)
        self.assertEqual(task.metrics.attempts, 3)
        self.assertEqual(task.result, "Success")
        self.assertEqual(mock_handler.call_count, 3)

    def test_task_retry_failure(self):
        """Test that a task fails after max retries"""

        mock_handler = Mock(side_effect=Exception("Always Fail"))

        async def async_handler():
            return mock_handler()

        self.orchestrator.add_task(name="fail_task", handler=async_handler, max_retries=2)

        with self.assertRaises(RuntimeError):
            asyncio.run(self.orchestrator.execute())

        task = self.orchestrator.tasks["fail_task"]
        self.assertEqual(task.status, TaskStatus.FAILURE)
        self.assertEqual(task.metrics.attempts, 2)
        self.assertEqual(mock_handler.call_count, 2)

    def test_task_timeout_retry(self):
        """Test that a task retries on timeout"""

        # First call sleeps longer than timeout, second call succeeds
        call_count = 0

        async def async_handler():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                await asyncio.sleep(0.2)  # Longer than timeout
            return "Success"

        self.orchestrator.add_task(
            name="timeout_task", handler=async_handler, max_retries=3, timeout_seconds=0.1
        )

        asyncio.run(self.orchestrator.execute())

        task = self.orchestrator.tasks["timeout_task"]
        self.assertEqual(task.status, TaskStatus.SUCCESS)
        self.assertEqual(task.metrics.attempts, 2)
        self.assertEqual(task.result, "Success")

    def test_pipeline_report_structure(self):
        """Test that get_report returns correct structure after execution"""

        async def simple_task():
            return "Done"

        self.orchestrator.add_task("task1", simple_task)
        asyncio.run(self.orchestrator.execute())

        report = self.orchestrator.get_report()

        self.assertEqual(report["status"], PipelineStatus.SUCCESS.value)
        self.assertIn("duration_seconds", report)
        self.assertIsNotNone(report["duration_seconds"])
        self.assertIn("tasks", report)
        self.assertIn("task1", report["tasks"])
        self.assertEqual(report["tasks"]["task1"]["status"], TaskStatus.SUCCESS.value)
        self.assertEqual(report["tasks"]["task1"]["metrics"]["attempts"], 1)


if __name__ == "__main__":
    unittest.main()
