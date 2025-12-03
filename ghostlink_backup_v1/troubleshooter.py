"""Automatic Troubleshooting and Error Correction for GhostLink.

This module provides autonomous error detection, diagnosis, and correction
capabilities for the GhostLink framework and Link agent.
"""
from __future__ import annotations

import asyncio
import json
import logging
import re
import subprocess
import sys
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = 0
    WARNING = 1
    ERROR = 2
    CRITICAL = 3


class ErrorCategory(Enum):
    """Error categories for classification."""
    IMPORT = "import"
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    NETWORK = "network"
    FILESYSTEM = "filesystem"
    PERMISSION = "permission"
    MEMORY = "memory"
    UNKNOWN = "unknown"


@dataclass
class ErrorReport:
    """Structured error report."""
    timestamp: datetime
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    traceback: str
    context: dict[str, Any] = field(default_factory=dict)
    suggested_fixes: list[str] = field(default_factory=list)
    auto_fixable: bool = False
    fix_applied: bool = False
    fix_result: Optional[str] = None


class AutoTroubleshooter:
    """Automatic troubleshooting and error correction system."""

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize troubleshooter.
        
        Args:
            workspace_root: Root directory of workspace
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.error_history: list[ErrorReport] = []
        self.fix_handlers: dict[ErrorCategory, list[Callable]] = {}
        self.auto_fix_enabled = True
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """Register default error fix handlers."""
        self.register_fix_handler(ErrorCategory.IMPORT, self._fix_missing_import)
        self.register_fix_handler(ErrorCategory.DEPENDENCY, self._fix_missing_dependency)
        self.register_fix_handler(ErrorCategory.CONFIGURATION, self._fix_configuration)
        self.register_fix_handler(ErrorCategory.PERMISSION, self._fix_permission)
        self.register_fix_handler(ErrorCategory.SYNTAX, self._fix_syntax_error)

    def register_fix_handler(
        self, 
        category: ErrorCategory, 
        handler: Callable[[ErrorReport], bool]
    ) -> None:
        """Register a fix handler for an error category.
        
        Args:
            category: Error category
            handler: Fix handler function that returns True if fixed
        """
        if category not in self.fix_handlers:
            self.fix_handlers[category] = []
        self.fix_handlers[category].append(handler)

    def analyze_error(self, error: Exception, context: Optional[dict] = None) -> ErrorReport:
        """Analyze an error and create a detailed report.
        
        Args:
            error: Exception to analyze
            context: Additional context information
            
        Returns:
            ErrorReport with diagnosis and suggested fixes
        """
        error_str = str(error)
        tb_str = traceback.format_exc()
        
        # Classify error
        category = self._classify_error(error, error_str, tb_str)
        severity = self._determine_severity(error, category)
        
        # Create report
        report = ErrorReport(
            timestamp=datetime.now(),
            category=category,
            severity=severity,
            message=error_str,
            traceback=tb_str,
            context=context or {}
        )
        
        # Analyze and suggest fixes
        self._analyze_and_suggest_fixes(report)
        
        # Store in history
        self.error_history.append(report)
        
        return report

    def _classify_error(self, error: Exception, error_str: str, tb_str: str) -> ErrorCategory:
        """Classify error into a category.
        
        Args:
            error: The exception
            error_str: String representation
            tb_str: Traceback string
            
        Returns:
            ErrorCategory classification
        """
        # Check exception type
        if isinstance(error, (ImportError, ModuleNotFoundError)):
            return ErrorCategory.IMPORT
        if isinstance(error, SyntaxError):
            return ErrorCategory.SYNTAX
        if isinstance(error, PermissionError):
            return ErrorCategory.PERMISSION
        if isinstance(error, FileNotFoundError):
            return ErrorCategory.FILESYSTEM
        if isinstance(error, MemoryError):
            return ErrorCategory.MEMORY
        if isinstance(error, (ConnectionError, TimeoutError)):
            return ErrorCategory.NETWORK
        
        # Check error message patterns
        if re.search(r"No module named|cannot import", error_str, re.I):
            return ErrorCategory.IMPORT
        if re.search(r"missing \d+ required.*argument|unexpected keyword", error_str, re.I):
            return ErrorCategory.CONFIGURATION
        if re.search(r"command not found|not recognized", error_str, re.I):
            return ErrorCategory.DEPENDENCY
        if re.search(r"permission denied|access denied", error_str, re.I):
            return ErrorCategory.PERMISSION
        if re.search(r"connection refused|timeout|network", error_str, re.I):
            return ErrorCategory.NETWORK
        
        return ErrorCategory.RUNTIME

    def _determine_severity(self, error: Exception, category: ErrorCategory) -> ErrorSeverity:
        """Determine error severity.
        
        Args:
            error: The exception
            category: Error category
            
        Returns:
            ErrorSeverity level
        """
        # Critical errors
        if isinstance(error, (MemoryError, SystemError)):
            return ErrorSeverity.CRITICAL
        if category == ErrorCategory.PERMISSION:
            return ErrorSeverity.ERROR
        
        # Errors that should be fixed
        if category in (ErrorCategory.IMPORT, ErrorCategory.DEPENDENCY, ErrorCategory.SYNTAX):
            return ErrorSeverity.ERROR
        
        # Configuration issues
        if category == ErrorCategory.CONFIGURATION:
            return ErrorSeverity.WARNING
        
        return ErrorSeverity.ERROR

    def _analyze_and_suggest_fixes(self, report: ErrorReport) -> None:
        """Analyze error and suggest fixes.
        
        Args:
            report: ErrorReport to populate with suggestions
        """
        msg = report.message.lower()
        
        # Import errors
        if report.category == ErrorCategory.IMPORT:
            match = re.search(r"no module named ['\"]([^'\"]+)['\"]", msg, re.I)
            if match:
                module = match.group(1)
                report.suggested_fixes.append(f"pip install {module}")
                report.auto_fixable = True
        
        # Dependency errors
        elif report.category == ErrorCategory.DEPENDENCY:
            if "python" in msg and "not found" in msg:
                report.suggested_fixes.extend([
                    "Install Python 3.8+ from python.org",
                    "Or install from Microsoft Store: python"
                ])
            elif "npm" in msg and "not recognized" in msg:
                report.suggested_fixes.append("Install Node.js from nodejs.org")
            elif "command not found" in msg or "not recognized" in msg:
                cmd_match = re.search(r"['\"]([^'\"]+)['\"]|(\w+)\s*:", msg)
                if cmd_match:
                    cmd = cmd_match.group(1) or cmd_match.group(2)
                    report.suggested_fixes.append(f"Install {cmd} via package manager")
        
        # Configuration errors
        elif report.category == ErrorCategory.CONFIGURATION:
            if "missing" in msg and "argument" in msg:
                report.suggested_fixes.append("Check function signature and required parameters")
            if "api_key" in msg or "token" in msg:
                report.suggested_fixes.extend([
                    "Set required API key in .env file",
                    "Check .env.example for required variables"
                ])
                report.auto_fixable = True
        
        # Permission errors
        elif report.category == ErrorCategory.PERMISSION:
            report.suggested_fixes.extend([
                "Run with appropriate permissions",
                "Check file/directory ownership and permissions"
            ])
        
        # Syntax errors
        elif report.category == ErrorCategory.SYNTAX:
            report.suggested_fixes.extend([
                "Run linter: make lint",
                "Format code: make format"
            ])
            report.auto_fixable = True

    async def auto_fix(self, report: ErrorReport) -> bool:
        """Attempt to automatically fix an error.
        
        Args:
            report: ErrorReport to fix
            
        Returns:
            True if fix was successful
        """
        if not self.auto_fix_enabled or not report.auto_fixable:
            return False
        
        handlers = self.fix_handlers.get(report.category, [])
        for handler in handlers:
            try:
                if await asyncio.get_event_loop().run_in_executor(None, handler, report):
                    report.fix_applied = True
                    report.fix_result = "Successfully applied automatic fix"
                    logger.info(f"Auto-fixed {report.category.value} error: {report.message}")
                    return True
            except Exception as e:
                logger.warning(f"Fix handler failed: {e}")
                continue
        
        return False

    def _fix_missing_import(self, report: ErrorReport) -> bool:
        """Fix missing import by installing package.
        
        Args:
            report: ErrorReport
            
        Returns:
            True if fixed
        """
        match = re.search(r"no module named ['\"]([^'\"]+)['\"]", report.message, re.I)
        if not match:
            return False
        
        module = match.group(1).split(".")[0]  # Get base module
        
        try:
            # Try to install with pip
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", module],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to install {module}: {e}")
            return False

    def _fix_missing_dependency(self, report: ErrorReport) -> bool:
        """Fix missing dependency.
        
        Args:
            report: ErrorReport
            
        Returns:
            True if fixed
        """
        # Check if it's a missing requirements.txt install
        req_file = self.workspace_root / "requirements.txt"
        if req_file.exists():
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                return result.returncode == 0
            except Exception as e:
                logger.error(f"Failed to install requirements: {e}")
        
        return False

    def _fix_configuration(self, report: ErrorReport) -> bool:
        """Fix configuration issues.
        
        Args:
            report: ErrorReport
            
        Returns:
            True if fixed
        """
        # Check for missing .env file
        env_file = self.workspace_root / ".env"
        env_example = self.workspace_root / ".env.example"
        
        if not env_file.exists() and env_example.exists():
            try:
                # Copy .env.example to .env
                env_file.write_text(env_example.read_text())
                logger.info("Created .env file from .env.example")
                return True
            except Exception as e:
                logger.error(f"Failed to create .env: {e}")
        
        return False

    def _fix_permission(self, report: ErrorReport) -> bool:
        """Attempt to fix permission issues.
        
        Args:
            report: ErrorReport
            
        Returns:
            True if fixed
        """
        # Extract file path from error
        match = re.search(r"['\"]([^'\"]+\.(py|json|txt|log))['\"]", report.message)
        if match:
            file_path = Path(match.group(1))
            if file_path.exists():
                try:
                    # Try to make file writable
                    file_path.chmod(0o644)
                    return True
                except Exception:
                    pass
        
        return False

    def _fix_syntax_error(self, report: ErrorReport) -> bool:
        """Attempt to fix syntax errors.
        
        Args:
            report: ErrorReport
            
        Returns:
            True if fixed
        """
        # Run auto-formatter
        try:
            result = subprocess.run(
                [sys.executable, "-m", "black", str(self.workspace_root / "ghostlink")],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                logger.info("Applied Black formatter to fix syntax")
                return True
        except Exception:
            pass
        
        return False

    def get_diagnostics(self) -> dict[str, Any]:
        """Get system diagnostics.
        
        Returns:
            Dictionary of diagnostic information
        """
        diagnostics = {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "workspace_root": str(self.workspace_root),
            "error_count": len(self.error_history),
            "errors_by_category": {},
            "errors_by_severity": {},
            "auto_fix_enabled": self.auto_fix_enabled,
            "fixes_applied": sum(1 for e in self.error_history if e.fix_applied)
        }
        
        # Count by category
        for cat in ErrorCategory:
            count = sum(1 for e in self.error_history if e.category == cat)
            if count > 0:
                diagnostics["errors_by_category"][cat.value] = count
        
        # Count by severity
        for sev in ErrorSeverity:
            count = sum(1 for e in self.error_history if e.severity == sev)
            if count > 0:
                diagnostics["errors_by_severity"][sev.name] = count
        
        return diagnostics

    def export_report(self, output_file: Optional[Path] = None) -> str:
        """Export error history to JSON report.
        
        Args:
            output_file: Optional output file path
            
        Returns:
            JSON report string
        """
        report = {
            "generated": datetime.now().isoformat(),
            "diagnostics": self.get_diagnostics(),
            "errors": [
                {
                    "timestamp": e.timestamp.isoformat(),
                    "category": e.category.value,
                    "severity": e.severity.name,
                    "message": e.message,
                    "traceback": e.traceback,
                    "context": e.context,
                    "suggested_fixes": e.suggested_fixes,
                    "auto_fixable": e.auto_fixable,
                    "fix_applied": e.fix_applied,
                    "fix_result": e.fix_result
                }
                for e in self.error_history
            ]
        }
        
        report_json = json.dumps(report, indent=2)
        
        if output_file:
            output_file.write_text(report_json)
            logger.info(f"Exported error report to {output_file}")
        
        return report_json


# Global troubleshooter instance
_troubleshooter: Optional[AutoTroubleshooter] = None


def get_troubleshooter() -> AutoTroubleshooter:
    """Get global troubleshooter instance.
    
    Returns:
        AutoTroubleshooter singleton
    """
    global _troubleshooter
    if _troubleshooter is None:
        _troubleshooter = AutoTroubleshooter()
    return _troubleshooter


async def handle_error(error: Exception, context: Optional[dict] = None, auto_fix: bool = True) -> ErrorReport:
    """Handle an error with automatic troubleshooting.
    
    Args:
        error: Exception to handle
        context: Additional context
        auto_fix: Whether to attempt automatic fix
        
    Returns:
        ErrorReport with diagnosis and fix attempts
    """
    troubleshooter = get_troubleshooter()
    report = troubleshooter.analyze_error(error, context)
    
    logger.error(
        f"Error detected: [{report.category.value}] {report.message}\n"
        f"Severity: {report.severity.name}\n"
        f"Suggested fixes: {', '.join(report.suggested_fixes)}"
    )
    
    if auto_fix and report.auto_fixable:
        fixed = await troubleshooter.auto_fix(report)
        if fixed:
            logger.info(f"Successfully auto-fixed error: {report.message}")
        else:
            logger.warning(f"Auto-fix failed for: {report.message}")
    
    return report
