"""Health monitoring and proactive error detection for GhostLink.

Monitors system health and detects potential issues before they cause errors.
"""
from __future__ import annotations

import asyncio
import logging
import os
import platform
import psutil
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class HealthStatus:
    """System health status."""
    timestamp: datetime
    overall_status: str  # "healthy", "warning", "critical"
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    issues: list[str]
    warnings: list[str]
    recommendations: list[str]


class HealthMonitor:
    """Monitor system health and detect issues."""

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize health monitor.
        
        Args:
            workspace_root: Root directory of workspace
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.check_interval = 60  # seconds
        self.monitoring = False
        self._monitor_task: Optional[asyncio.Task] = None

    async def check_health(self) -> HealthStatus:
        """Perform comprehensive health check.
        
        Returns:
            HealthStatus with current system state
        """
        issues = []
        warnings = []
        recommendations = []
        
        # Check system resources
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(str(self.workspace_root))
        
        # CPU checks
        if cpu_usage > 90:
            issues.append(f"Critical CPU usage: {cpu_usage}%")
            recommendations.append("Close unnecessary applications")
        elif cpu_usage > 70:
            warnings.append(f"High CPU usage: {cpu_usage}%")
        
        # Memory checks
        if memory.percent > 90:
            issues.append(f"Critical memory usage: {memory.percent}%")
            recommendations.append("Close memory-intensive applications")
        elif memory.percent > 75:
            warnings.append(f"High memory usage: {memory.percent}%")
        
        # Disk checks
        if disk.percent > 95:
            issues.append(f"Critical disk usage: {disk.percent}%")
            recommendations.append("Free up disk space")
        elif disk.percent > 85:
            warnings.append(f"High disk usage: {disk.percent}%")
        
        # Check Python installation
        python_issues = self._check_python()
        issues.extend(python_issues)
        
        # Check dependencies
        dep_issues, dep_warnings = self._check_dependencies()
        issues.extend(dep_issues)
        warnings.extend(dep_warnings)
        
        # Check configuration
        config_issues = self._check_configuration()
        issues.extend(config_issues)
        
        # Check file permissions
        perm_issues = self._check_permissions()
        issues.extend(perm_issues)
        
        # Determine overall status
        if issues:
            overall = "critical"
        elif warnings:
            overall = "warning"
        else:
            overall = "healthy"
        
        return HealthStatus(
            timestamp=datetime.now(),
            overall_status=overall,
            cpu_usage=cpu_usage,
            memory_usage=memory.percent,
            disk_usage=disk.percent,
            issues=issues,
            warnings=warnings,
            recommendations=recommendations
        )

    def _check_python(self) -> list[str]:
        """Check Python installation and version.
        
        Returns:
            List of issues found
        """
        issues = []
        
        # Check Python version
        version = sys.version_info
        if version < (3, 8):
            issues.append(
                f"Python {version.major}.{version.minor} is too old. "
                "GhostLink requires Python 3.8+"
            )
        
        # Check pip
        try:
            import pip  # noqa: F401
        except ImportError:
            issues.append("pip is not installed")
        
        return issues

    def _check_dependencies(self) -> tuple[list[str], list[str]]:
        """Check required dependencies.
        
        Returns:
            Tuple of (issues, warnings)
        """
        issues = []
        warnings = []
        
        # Check required packages
        required = ["fastapi", "httpx", "pydantic", "sqlalchemy", "click"]
        for package in required:
            try:
                __import__(package)
            except ImportError:
                issues.append(f"Required package '{package}' is not installed")
        
        # Check optional packages
        optional = ["black", "ruff", "mypy", "pytest"]
        for package in optional:
            try:
                __import__(package)
            except ImportError:
                warnings.append(f"Optional package '{package}' is not installed")
        
        # Check Node.js (for VS Code extension)
        if not shutil.which("node"):
            warnings.append("Node.js not found - VS Code extension won't compile")
        
        # Check npm
        if not shutil.which("npm"):
            warnings.append("npm not found - VS Code extension dependencies can't be installed")
        
        return issues, warnings

    def _check_configuration(self) -> list[str]:
        """Check configuration files.
        
        Returns:
            List of issues found
        """
        issues = []
        
        # Check .env file
        env_file = self.workspace_root / ".env"
        env_example = self.workspace_root / ".env.example"
        
        if not env_file.exists():
            if env_example.exists():
                issues.append(
                    ".env file not found. Copy .env.example to .env and configure"
                )
            else:
                issues.append(".env file not found and no .env.example available")
        
        # Check pyproject.toml
        pyproject = self.workspace_root / "pyproject.toml"
        if not pyproject.exists():
            issues.append("pyproject.toml not found - package may not be properly configured")
        
        return issues

    def _check_permissions(self) -> list[str]:
        """Check file and directory permissions.
        
        Returns:
            List of issues found
        """
        issues = []
        
        # Check if workspace is writable
        test_file = self.workspace_root / ".write_test"
        try:
            test_file.write_text("test")
            test_file.unlink()
        except Exception:
            issues.append(f"Workspace directory is not writable: {self.workspace_root}")
        
        # Check log directory
        log_dir = self.workspace_root / "logs"
        if log_dir.exists() and not os.access(log_dir, os.W_OK):
            issues.append(f"Log directory is not writable: {log_dir}")
        
        return issues

    async def start_monitoring(self) -> None:
        """Start continuous health monitoring."""
        if self.monitoring:
            return
        
        self.monitoring = True
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info("Health monitoring started")

    async def stop_monitoring(self) -> None:
        """Stop health monitoring."""
        self.monitoring = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("Health monitoring stopped")

    async def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.monitoring:
            try:
                status = await self.check_health()
                
                if status.overall_status == "critical":
                    logger.error(
                        f"CRITICAL HEALTH STATUS\n"
                        f"Issues: {', '.join(status.issues)}\n"
                        f"Recommendations: {', '.join(status.recommendations)}"
                    )
                elif status.overall_status == "warning":
                    logger.warning(
                        f"Health warnings detected: {', '.join(status.warnings)}"
                    )
                else:
                    logger.debug("System health: OK")
                
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                await asyncio.sleep(self.check_interval)

    def get_system_info(self) -> dict[str, Any]:
        """Get comprehensive system information.
        
        Returns:
            Dictionary of system information
        """
        return {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
            },
            "python": {
                "version": sys.version,
                "executable": sys.executable,
                "prefix": sys.prefix,
            },
            "resources": {
                "cpu_count": psutil.cpu_count(),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_total_gb": round(psutil.disk_usage(str(self.workspace_root)).total / (1024**3), 2),
                "disk_free_gb": round(psutil.disk_usage(str(self.workspace_root)).free / (1024**3), 2),
                "disk_percent": psutil.disk_usage(str(self.workspace_root)).percent,
            },
            "workspace": {
                "root": str(self.workspace_root),
                "exists": self.workspace_root.exists(),
                "writable": os.access(self.workspace_root, os.W_OK),
            }
        }


# Global health monitor instance
_health_monitor: Optional[HealthMonitor] = None


def get_health_monitor() -> HealthMonitor:
    """Get global health monitor instance.
    
    Returns:
        HealthMonitor singleton
    """
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = HealthMonitor()
    return _health_monitor
