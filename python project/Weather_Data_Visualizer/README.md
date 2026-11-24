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

### Key Objectives Achieved:
- **Import Weather Records**: Ingest data seamlessly from CSV files with structural validation and header checks.
- **Robust Input & Data Validation**: Validate ranges, data types, formats, and detect malformed inputs with configurable limits.
- **Statistical Analytics**: Calculate mean, min, max, cumulative rainfall, rainy days count, and trend trajectories.
- **Visual Trend Charts**: Render temperature line graphs, daily rainfall bar charts, and multi-variable comparison dashboards using Matplotlib.
- **Dual Persistence**: Persist and restore records using both CSV and JSON formats with backup and recovery support.
- **Multi-Criteria Search & Filter**: Search by city, date, date range, temperature threshold, rainfall interval, and keyword.
- **Threshold Warnings & Advisories**: Detect heatwaves, cold frost, heavy rainfall, and sudden day-to-day temperature shifts.
- **Multi-Format Report Export**: Export analysis in CSV, plain text, and Markdown formats.

---

## 2. Project Architecture & Directory Structure

The project strictly follows a clean, modular architecture:

```
Weather_Data_Visualizer/
│
├── main.py                     # Main application entry point & lifecycle manager
├── requirements.txt            # Project dependencies (matplotlib, pytest)
├── README.md                   # Complete project documentation
├── .gitignore                  # Git ignore definitions
├── run.bat                     # 1-click Windows launcher
├── pytest.ini                  # Pytest configuration
│
├── data/                       # Local data storage
│   ├── sample_weather.csv      # Initial reference dataset (Hyderabad, etc.)
│   ├── weather_data.csv        # Active CSV working storage
│   ├── weather_data.json       # Active JSON working storage
│   └── backups/                # Timestamped backup files
│
├── src/                        # Core application modules
│   ├── __init__.py             # Package marker
│   ├── menu.py                 # Interactive CLI menu & formatted table display
│   ├── input_handler.py        # Safe user input collection & retry handling
│   ├── validator.py            # Record & field validation engine
│   ├── data_loader.py          # CSV import & header verification
│   ├── data_processor.py       # Data cleaning, sorting & preparation
│   ├── storage.py              # Dual CSV/JSON persistence & backups
│   ├── search.py               # Multi-parameter search & filtering
│   ├── analytics.py            # Statistical metrics & trend calculations
│   ├── visualizer.py           # Matplotlib chart plotting engine
│   ├── exporter.py             # CSV, TXT, and Markdown report generator
│   └── alerts.py               # Data anomaly & threshold warnings
│
├── charts/                     # Generated graphical output
│   ├── temperature_trend.png   # Line chart of temperature over time
│   ├── rainfall_trend.png      # Daily rainfall bar chart with mean line
│   ├── weather_comparison.png  # Multi-city or multi-metric comparison
│   └── weather_dashboard.png   # 4-panel comprehensive dashboard
│
├── reports/                    # Exported analysis summaries
│   ├── summary_report.txt      # Formatted plain text report
│   ├── summary_report.md       # GitHub-flavored Markdown report
│   └── analysis_report.csv     # Structured tabular analysis spreadsheet
│
├── tests/                      # Pytest unit testing suite (43 passing tests)
│   ├── conftest.py             # Test path configuration
│   ├── test_validator.py       # Validation logic tests
│   ├── test_data_loader.py     # Loader & CSV structure tests
│   ├── test_analytics.py       # Mathematical & statistical tests
│   ├── test_storage.py         # Persistence, recovery & backup tests
│   └── test_additional_modules.py # Processor, search, and exporter tests
│
└── docs/                       # Detailed documentation
    ├── project_architecture.md # In-depth technical architecture & data flow
    └── user_guide.md           # Step-by-step user guide & demo script
```

---

## 3. Installation & Setup

### Requirements
- Python 3.10 or higher (Python 3.13 tested and verified)
- Matplotlib (`>= 3.7.0`)
- Pytest (`>= 7.0.0`)

### Setup on Windows

1. Open PowerShell or Command Prompt and navigate to the project directory:
   ```powershell
   cd Weather_Data_Visualizer
   ```

2. *(Optional)* Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install required packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Launch the application:
   ```powershell
   python main.py
   ```
   *Alternatively, double click `run.bat` for instant startup.*

---

## 4. Running the Test Suite

The project includes 43 unit tests covering all modules with 100% pass rate:

```powershell
python -m pytest tests -v
```

Output:
```
============================= test session starts =============================
platform win32 -- Python 3.13.15, pytest-9.2.0
collected 43 items

tests/test_validator.py::... PASSED
tests/test_data_loader.py::... PASSED
tests/test_analytics.py::... PASSED
tests/test_storage.py::... PASSED
tests/test_additional_modules.py::... PASSED

============================= 43 passed in 0.24s ==============================
```

---

## 5. Live Demo Script (Step-by-Step)

| Step | Action | What to Showcase |
| :---: | :--- | :--- |
| **1. Launch** | Run `python main.py` | Styled startup banner, automatic state loading, and main menu. |
| **2. Import Data** | Select Option `1` | Ingests sample data, normalizes records, and confirms row count. |
| **3. Validation** | Select Option `4` | Enter invalid date or negative rain; show instant error recovery without crash. |
| **4. Analytics** | Select Option `6` | Display average, min, max temperature, rainy days, and trend slope. |
| **5. Charts** | Select Options `7`, `8`, `9` | Generates high-res PNG charts in `charts/` directory. |
| **6. Reports** | Select Option `10` | Exports formatted `summary_report.txt`, `summary_report.md`, and `analysis_report.csv`. |
| **7. Persistence** | Exit (`0`) and re-launch | Auto-saved data persists cleanly upon restart. |

---

## 6. Sample Dataset Reference

Included in `data/sample_weather.csv`:

```csv
date,city,temperature,rainfall,humidity,wind_speed
2026-11-01,Hyderabad,29.5,0.0,48,12.5
2026-11-02,Hyderabad,30.1,2.4,55,14.2
2026-11-03,Hyderabad,28.7,5.2,61,11.8
2026-11-04,Hyderabad,27.9,0.0,52,10.4
2026-11-05,Hyderabad,31.2,0.0,43,15.1
2026-11-06,Hyderabad,26.8,8.6,67,9.7
2026-11-07,Hyderabad,29.0,1.3,58,13.0
```

---

## 7. License & Credits

- **CampusSolve Project #91**: Weather Data Visualizer
- **Author**: CampusSolve Student Development Team
- **License**: MIT Open Source License
