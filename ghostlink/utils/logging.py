"""Logging Configuration for GhostLink"""

import sys
from pathlib import Path

from loguru import logger

from .config import config


def setup_logging(level: str = None, log_file: str = None):
    """Setup comprehensive logging configuration"""
    # Remove default handler
    logger.remove()

    # Get configuration
    if level is None:
        level = config.get("logging.level", "INFO")

    if log_file is None:
        log_dir = Path(config.get("logging.directory", "logs"))
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / config.get("logging.filename", "ghostlink.log")

    # Console handler with colors
    logger.add(
        sys.stdout,
        level=level,
        format=config.get(
            "logging.format",
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>",
        ),
        colorize=True,
    )

    # File handler with rotation and compression
    logger.add(
        log_file,
        level=level,
        format=config.get(
            "logging.format",
            "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | " "{name}:{function}:{line} | {message}",
        ),
        rotation=config.get("logging.rotation", "10 MB"),
        retention=config.get("logging.retention", "1 week"),
        compression=config.get("logging.compression", "gz"),
    )

    logger.info("GhostLink logging initialized")
    return logger
