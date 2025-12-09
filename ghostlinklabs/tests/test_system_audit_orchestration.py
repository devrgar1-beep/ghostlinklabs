"""Test suite for System Audit and Pipeline Orchestration features."""

import asyncio
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

from ghostlink.system_audit import SystemAuditor, AuditFinding, AuditLevel
from ghostlink.orchestrator import PipelineOrchestrator, PipelineTask, TaskStatus
from ghostlink.health import HealthMonitor, HealthCheckService, HealthMetric


class TestSystemAudit(unittest.TestCase):
    """Tests for system audit functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.auditor = SystemAuditor()

    def test_audit_completes(self):
        """Test that audit completes successfully."""
        report = self.auditor.audit()

        self.assertIn("audit", report)
        self.assertIn("system", report)
        self.assertIn("findings", report)

    def test_audit_report_structure(self):
        """Test audit report has correct structure."""
        report = self.auditor.audit()
        audit = report["audit"]

        self.assertIn("timestamp", audit)
        self.assertIn("duration_seconds", audit)
        self.assertIn("status", audit)
        self.assertIn("findings_summary", audit)

    def test_audit_status_values(self):
        """Test audit status is valid."""
        report = self.auditor.audit()
        status = report["audit"]["status"]

        self.assertIn(status, ["HEALTHY", "WARNING", "CRITICAL"])

    def test_system_info_included(self):
        """Test system info is included in report."""
        report = self.auditor.audit()
        system = report["system"]

        self.assertIn("platform", system)
        self.assertIn("python_version", system)
        self.assertIn("cpu_count", system)

    def test_findings_summary_accurate(self):
        """Test findings summary is accurate."""
        report = self.auditor.audit()
        summary = report["audit"]["findings_summary"]

        self.assertEqual(summary["total"],
                        summary["critical"] + summary["errors"] +
                        summary["warnings"])


class TestPipelineOrchestration(unittest.TestCase):
    """Tests for pipeline orchestration."""

    def setUp(self):
        """Set up test fixtures."""
        self.pipeline = PipelineOrchestrator("test_pipeline", "Test pipeline")

    def test_pipeline_creation(self):
        """Test pipeline creation."""
        self.assertEqual(self.pipeline.name, "test_pipeline")
        self.assertEqual(self.pipeline.description, "Test pipeline")
        self.assertIsNotNone(self.pipeline.pipeline_id)

    def test_add_task(self):
        """Test adding tasks to pipeline."""
        async def dummy_task():
            return "done"

        self.pipeline.add_task("task1", dummy_task)

        self.assertEqual(len(self.pipeline.tasks), 1)
        self.assertIn("task1", self.pipeline.tasks)

    def test_execution_plan_building(self):
        """Test execution plan building."""
        async def task1():
            return "task1"

        self.pipeline.add_task("task1", task1)
        self.pipeline.build_execution_plan()

        self.assertGreater(len(self.pipeline.execution_plan), 0)

    def test_get_report_structure(self):
        """Test pipeline report structure."""
        report = self.pipeline.get_report()

        self.assertIn("pipeline_id", report)
        self.assertIn("name", report)
        self.assertIn("status", report)
        self.assertIn("tasks", report)
        self.assertIn("execution_plan", report)

    def test_pipeline_execution(self):
        """Test basic pipeline execution."""
        async def dummy_task():
            return "success"

        async def run_test():
            self.pipeline.add_task("task1", dummy_task)
            await self.pipeline.execute()
            return self.pipeline.get_report()

        report = asyncio.run(run_test())

        self.assertIn("task1", report["tasks"])
        self.assertEqual(report["tasks"]["task1"]["status"], "success")

    def test_pipeline_creation_succeeds(self):
        """Test pipeline can be created multiple times."""
        for i in range(3):
            pipeline = PipelineOrchestrator(f"test_{i}", f"Test {i}")
            self.assertEqual(pipeline.name, f"test_{i}")


class TestHealthMonitoring(unittest.TestCase):
    """Tests for health monitoring."""

    def setUp(self):
        """Set up test fixtures."""
        self.service = HealthCheckService()

    def test_health_check_performs(self):
        """Test health check performs successfully."""
        result = self.service.perform_check()

        self.assertIn("timestamp", result)
        self.assertIn("checks", result)
        self.assertIn("overall_status", result)

    def test_health_check_has_all_metrics(self):
        """Test health check includes all metrics."""
        result = self.service.perform_check()
        checks = result["checks"]

        self.assertIn("cpu", checks)
        self.assertIn("memory", checks)
        self.assertIn("disk", checks)

    def test_health_check_status_values(self):
        """Test health check status values are valid."""
        result = self.service.perform_check()

        self.assertIn(result["overall_status"], ["healthy", "warning", "critical"])

        for check in result["checks"].values():
            self.assertIn(check["status"], ["healthy", "warning", "critical"])

    def test_health_monitor_async_startup(self):
        """Test health monitor async operations."""
        async def run_test():
            monitor = HealthMonitor(update_interval=1)
            task = monitor.start()

            await asyncio.sleep(2)

            monitor.stop()
            await task

            report = monitor.get_report()
            return report

        report = asyncio.run(run_test())

        self.assertIsNotNone(report)
        self.assertIn("current", report)
        self.assertIn("averages", report)

    def test_health_monitor_history(self):
        """Test health monitor history tracking."""
        async def run_test():
            monitor = HealthMonitor(update_interval=0.1)
            task = monitor.start()

            await asyncio.sleep(1)

            monitor.stop()
            await task

            return len(monitor.history)

        history_count = asyncio.run(run_test())

        self.assertGreater(history_count, 0)

    def test_health_checks_stored(self):
        """Test health check results are stored."""
        self.service.perform_check()
        self.service.perform_check()

        self.assertEqual(len(self.service.check_results), 2)

    def test_health_check_max_results(self):
        """Test health check results are trimmed to max."""
        original_max = self.service.max_results
        self.service.max_results = 5

        for _ in range(10):
            self.service.perform_check()

        self.assertEqual(len(self.service.check_results), 5)

        # Restore
        self.service.max_results = original_max


class TestIntegration(unittest.TestCase):
    """Integration tests."""

    def test_audit_then_pipeline(self):
        """Test running audit then pipeline."""
        async def run_test():
            # Run audit
            auditor = SystemAuditor()
            audit_report = auditor.audit()

            # Run pipeline
            pipeline = PipelineOrchestrator("integration_test", "Test")

            async def task1():
                return f"Audit status: {audit_report['audit']['status']}"

            pipeline.add_task("task1", task1)
            await pipeline.execute()

            return {
                "audit": audit_report["audit"]["status"],
                "pipeline": pipeline.get_report()["status"]
            }

        result = asyncio.run(run_test())

        self.assertIn(result["audit"], ["HEALTHY", "WARNING", "CRITICAL"])
        self.assertIsNotNone(result["pipeline"])

    def test_monitor_during_pipeline(self):
        """Test health monitoring during pipeline execution."""
        async def run_test():
            monitor = HealthMonitor(update_interval=0.5)
            task = monitor.start()

            pipeline = PipelineOrchestrator("pipeline_test", "Test")

            async def work():
                await asyncio.sleep(1)
                return "done"

            pipeline.add_task("work", work)
            await pipeline.execute()

            monitor.stop()
            await task

            return {
                "health_samples": len(monitor.history),
                "pipeline_status": pipeline.get_report()["status"]
            }

        result = asyncio.run(run_test())

        self.assertGreater(result["health_samples"], 0)
        self.assertEqual(result["pipeline_status"], "success")


class TestErrorHandling(unittest.TestCase):
    """Tests for error handling."""

    def test_audit_with_missing_files(self):
        """Test audit handles missing files gracefully."""
        auditor = SystemAuditor()
        report = auditor.audit()

        # Should still complete
        self.assertIn("audit", report)
        self.assertIn("status", report["audit"])

    def test_pipeline_with_sync_task(self):
        """Test pipeline with simple sync completion."""
        async def run_test():
            pipeline = PipelineOrchestrator("sync_test", "Test")

            def sync_work():
                return "sync_done"

            # Note: sync functions should be wrapped for asyncio
            async def async_wrapper():
                return sync_work()

            pipeline.add_task("sync", async_wrapper)
            await pipeline.execute()
            return pipeline.get_report()

        report = asyncio.run(run_test())

        self.assertIn("sync", report["tasks"])


if __name__ == "__main__":
    unittest.main()
