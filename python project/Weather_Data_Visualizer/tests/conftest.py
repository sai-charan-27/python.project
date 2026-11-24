"""
Pytest configuration for Weather Data Visualizer.
Ensures src/ and project root are always discoverable.
"""

import sys
from pathlib import Path

# Add project root directory to sys.path
PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))
