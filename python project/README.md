# Weather Data Visualizer

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Matplotlib](https://img.shields.io/badge/visualization-matplotlib-orange.svg)](https://matplotlib.org/)
[![Pytest Passed](https://img.shields.io/badge/tests-43%2F43%20passed-brightgreen.svg)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **CampusSolve Project #91 | Data & Visualization**  
> **Technologies:** Python · CSV · JSON · Matplotlib · Pytest

---

## 1. Project Overview

**Weather Data Visualizer** is a modular, standalone Python application that empowers users to load historical weather observations, analyze meteorological statistics, visualize temperature and rainfall trends through publication-quality charts, and export structured reports — all with **zero dependency on external web APIs or cloud services**.

---

## 2. Quick Launch on Windows

You can launch the project directly from this root directory or from inside `Weather_Data_Visualizer`:

### Option A: Direct Launch
```powershell
python main.py
```
*(Or double-click `run.bat`)*

### Option B: From `Weather_Data_Visualizer` Directory
```powershell
cd Weather_Data_Visualizer
python main.py
```

### Run Tests:
```powershell
python -m pytest Weather_Data_Visualizer/tests -v
```

---

## 3. Directory Layout

The complete project code and assets are located inside `Weather_Data_Visualizer/`:

```
Weather_Data_Visualizer/
├── main.py                     # Main application entry point
├── requirements.txt            # Project dependencies
├── README.md                   # Full project documentation
├── run.bat                     # Windows batch launcher
├── data/                       # CSV and JSON datasets
├── src/                        # 12 Modular Python components
├── charts/                     # Generated Matplotlib graphs
├── reports/                    # Exported CSV, TXT, and Markdown reports
├── tests/                      # Pytest unit tests (43 passed)
└── docs/                       # Project architecture and User Guide
```

For full details, please refer to:
- [Architecture Guide](file:///c:/Users/SAI%20CHARAN/Desktop/python%20project/Weather_Data_Visualizer/docs/project_architecture.md)
- [User Guide & Demo Walkthrough](file:///c:/Users/SAI%20CHARAN/Desktop/python%20project/Weather_Data_Visualizer/docs/user_guide.md)
