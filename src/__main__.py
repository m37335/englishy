"""
Main entry point for running the Streamlit app.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the Streamlit app
from app.app import main

if __name__ == "__main__":
    main() 