"""
Logging utilities for Englishy.
"""

from loguru import logger

# Configure loguru logger
logger.add(
    "logs/englishy.log",
    rotation="1 day",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
) 