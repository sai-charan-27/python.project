"""
Weather Data Visualizer
CampusSolve Project #91
Root Workspace Launcher
"""

import sys
import os
from pathlib import Path

# Switch working directory to Weather_Data_Visualizer project folder
project_dir = Path(__file__).resolve().parent / "Weather_Data_Visualizer"
if project_dir.exists():
    os.chdir(str(project_dir))
    if str(project_dir) not in sys.path:
        sys.path.insert(0, str(project_dir))

import main

if __name__ == "__main__":
    main.main()
