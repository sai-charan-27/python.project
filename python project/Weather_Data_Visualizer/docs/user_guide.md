# Weather Data Visualizer - User Guide & Demo Playbook

## CampusSolve Project #91 | Python · CSV · JSON · Matplotlib

---

## 1. Quick Start

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Windows / Linux / macOS terminal

### Launching the Application

From Windows PowerShell or Command Prompt:

```bash
cd "Weather_Data_Visualizer"
py -3.13 main.py
```
*(Or double-click `run.bat` for one-click startup on Windows)*

---

## 2. Recommended Hackathon Demo Walkthrough

Follow these 7 sequential steps to deliver an impressive live demonstration:

### Step 1 — Launch
1. Start the application:
   ```bash
   python main.py
   ```
2. Present the styled welcome banner and main numbered menu. Note how the application automatically reports the number of loaded records upon launch.

### Step 2 — Import Data
1. From the menu, enter `1` to **Load sample weather data**.
2. Notice the confirmation message showing that the sample records from Hyderabad and surrounding regions have been imported and normalized.

### Step 3 — Demonstrate Validation
1. Choose menu option `4` (**Add a new weather record**).
2. Input an invalid date, such as `2026/11/31` or `invalid-date`.
   - Observe how the input handler catches the format mismatch and asks for re-entry without crashing!
3. Input a valid date: `2026-11-15`.
4. City: `Hyderabad`.
5. Enter an invalid temperature, e.g., `85` (above the configured max 60°C).
   - Observe the immediate validation message: `Error: Value must be at most 60.0.`
6. Enter a valid temperature, e.g., `28.5`.
7. Input a negative rainfall value like `-10`.
   - Observe the non-negative rainfall enforcement!
8. Enter valid values for rainfall (`4.0`), humidity (`60`), and wind speed (`12.0`).
   - The record is validated, sorted chronologically, and appended!

### Step 4 — Run Statistical Analytics
1. Select menu option `6` (**Display statistical analytics**).
2. Review the comprehensive statistical report:
   - **Temperature**: Mean temperature, maximum record with city and date, minimum record, and trend slope.
   - **Precipitation**: Total cumulative rainfall, daily average, and rainy days count (days with $\ge 0.1$ mm).
   - **Humidity & Wind**: Mean humidity, average wind velocity, and peak gust.

### Step 5 — Display & Generate Charts
1. Select menu option `7` (**Generate & view temperature charts**).
   - Saved to `charts/temperature_trend.png`.
2. Select menu option `8` (**Generate & view rainfall charts**).
   - Saved to `charts/rainfall_trend.png`.
3. Select menu option `9` (**Generate & view humidity & comparison charts**).
   - Generates `charts/weather_comparison.png` and `charts/weather_dashboard.png`.
4. Open the `charts/` folder to view the high-resolution, color-coded visual charts.

### Step 6 — Export Reports
1. Select menu option `10` (**Export reports**).
2. The application compiles:
   - `reports/analysis_report.csv`: Complete spreadsheet with summary header and row details.
   - `reports/summary_report.txt`: Clean, human-readable ASCII summary.
   - `reports/summary_report.md`: GitHub-ready Markdown report with tables and alert badges.

### Step 7 — Verify Data Persistence
1. Select menu option `12` to manually save records, or simply select `0` to **Exit**.
   - Notice the shutdown auto-save notification:
     `[✓] Session state auto-saved to CSV and JSON.`
2. Restart the application:
   ```bash
   python main.py
   ```
3. Observe that the startup banner immediately shows:
   `[*] Initialized: Loaded 29 existing records from 'weather_data.csv'.`
4. Choose option `3` (**View all weather records**) to confirm that your newly added records persist seamlessly across sessions.

---

## 3. Menu Options Reference

| Option | Name | Description |
| :---: | :--- | :--- |
| `1` | **Load sample weather data** | Reads default records from `data/sample_weather.csv`. |
| `2` | **Import external weather CSV** | Imports any user-specified CSV file path with column validation. |
| `3` | **View all weather records** | Displays tabular view of records with pagination (15 per page). |
| `4` | **Add a new weather record** | Interactive step-by-step entry with real-time input verification. |
| `5` | **Search and filter records** | Search by city, date/range, temperature, rainfall, or keyword. |
| `6` | **Display analytics** | Calculates descriptive statistics, trends, and rainy days. |
| `7` | **Generate temperature charts** | Plots temperature line chart with annotations for min/max points. |
| `8` | **Generate rainfall charts** | Plots daily rainfall bar chart with average reference line. |
| `9` | **Comparison & dashboard charts** | Dual-axis temperature vs rainfall and 4-panel dashboard. |
| `10` | **Export reports** | Exports CSV, TXT, and Markdown reports to `reports/`. |
| `11` | **View threshold warnings** | Identifies heat, frost, torrential rain, and rapid shifts. |
| `12` | **Save records to disk** | Writes active dataset to `data/weather_data.csv` and `.json`. |
| `13` | **Backup & restore** | Creates timestamped backups and restores previous versions. |
| `14` | **Configure thresholds** | Modifies min/max temperature, wind, and rainfall bounds. |
| `0` | **Exit Application** | Performs auto-save and cleanly terminates session. |
