"""
Logging utilities for Englishy.
"""

import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure standard logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
    handlers=[
        logging.FileHandler("logs/englishy.log"),
        logging.StreamHandler()
    ]
)

# Create logger instance
logger = logging.getLogger("englishy") 