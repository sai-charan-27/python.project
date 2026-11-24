# Weather Data Visualizer - Project Architecture

## CampusSolve Project #91 | Data & Visualization

---

## 1. High-Level Architecture Overview

The **Weather Data Visualizer** is a modular Python CLI application designed for high reliability, extensibility, and zero external cloud dependency. It implements clean separation of concerns across 12 specialized modules.

```mermaid
flowchart TD
    User([User / CLI Terminal]) <--> Menu[Module 2: menu.py & Module 3: input_handler.py]
    
    subgraph Core Processing Engine
        Loader[Module 5: data_loader.py] --> Validator[Module 4: validator.py]
        Validator --> Processor[Module 6: data_processor.py]
    end

    subgraph Persistence Layer
        Storage[Module 7: storage.py]
        CSV[(CSV Files)]
        JSON[(JSON Files)]
        Storage <--> CSV
        Storage <--> JSON
    end

    subgraph Analytics & Insights
        Search[Module 8: search.py]
        Analytics[Module 9: analytics.py]
        Alerts[Module 12: alerts.py]
    end

    subgraph Visualization & Reporting
        Visualizer[Module 10: visualizer.py] --> Charts[Charts: PNG Trend Graphs]
        Exporter[Module 11: exporter.py] --> Reports[Reports: CSV, TXT, MD]
    end

    Menu --> Loader
    Menu --> Search
    Menu --> Analytics
    Menu --> Alerts
    Menu --> Visualizer
    Menu --> Exporter
    Menu <--> Storage

    Processor --> Storage
    Processor --> Analytics
```

---

## 2. Module Specifications

| Module | File | Responsibility |
| :--- | :--- | :--- |
| **Module 1: Main Application** | `main.py` | Initializes state, sets paths, loads stored records, and manages lifecycle. |
| **Module 2: Interactive Menu** | `src/menu.py` | Renders ASCII menus, tables with pagination, and dispatches options. |
| **Module 3: Input Handler** | `src/input_handler.py` | Safe terminal prompts with type casting, bounds checking, and graceful retries. |
| **Module 4: Validation Engine** | `src/validator.py` | Configurable range validation, date parsing, column checks, and record verification. |
| **Module 5: Data Loader** | `src/data_loader.py` | Reads external or sample CSVs, verifies headers, detects malformed rows. |
| **Module 6: Data Processor** | `src/data_processor.py` | Deduplication, type normalization, chronological sorting, and array extraction. |
| **Module 7: Storage Engine** | `src/storage.py` | Dual CSV/JSON persistence, backup generation, corrupted file recovery. |
| **Module 8: Search & Filter** | `src/search.py` | City substring search, date ranges, temperature and rainfall thresholds. |
| **Module 9: Analytics Engine** | `src/analytics.py` | Mean, min, max, rainfall sums, rainy day counts, and trend slopes. |
| **Module 10: Visualization** | `src/visualizer.py` | Matplotlib line/bar/comparison charts rendered with high DPI. |
| **Module 11: Report Exporter** | `src/exporter.py` | Compiles analysis and alerts into CSV, plain text, and Markdown reports. |
| **Module 12: Threshold Alerts** | `src/alerts.py` | Evaluates heatwaves, torrential rain, arid/muggy humidity, and sudden shifts. |

---

## 3. Data Flow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Menu as Interactive Menu
    participant Loader as Data Loader
    participant Validator as Validator
    participant Processor as Data Processor
    participant Storage as Storage (CSV/JSON)
    participant Analytics as Analytics & Alerts
    participant Visualizer as Visualizer & Exporter

    User->>Menu: 1. Selects 'Load Sample Data' or 'Import CSV'
    Menu->>Loader: Read raw file content
    Loader->>Validator: Validate column headers and data types
    Validator-->>Loader: Return valid rows & validation report
    Loader->>Processor: Normalize and sort chronologically
    Processor-->>Menu: Update active state in-memory
    
    User->>Menu: 2. Selects 'Run Analytics' or 'Generate Charts'
    Menu->>Analytics: Compute statistical summary & evaluate thresholds
    Analytics-->>Menu: Formatted metrics & trend indicators
    Menu->>Visualizer: Plot temperature / rainfall charts
    Visualizer-->>User: Save high-res PNG to charts/ folder

    User->>Menu: 3. Selects 'Export Reports'
    Menu->>Visualizer: Export to reports/ (CSV, TXT, MD)
    Menu->>Storage: Auto-save state on exit to data/weather_data.csv & .json
```

---

## 4. Non-Functional & Reliability Architecture

1. **Graceful Degradation**:
   - The application never crashes when encountering corrupted data rows or missing files. Invalid rows are recorded and reported to the user while valid rows continue to be processed.
2. **Configurable Thresholds**:
   - No arbitrary hardcoded meteorological limits. Valid temperature spans, wind speed bounds, and rainy-day definitions can be configured in `DEFAULT_CONFIG` or dynamically via Option 14 in the menu.
3. **Dual Persistence**:
   - Stores identical data in both CSV (`data/weather_data.csv`) for tabular spreadsheet portability and JSON (`data/weather_data.json`) for programmatic tree persistence.
4. **Resilient Matplotlib Engine**:
   - Configured with headless backend (`Agg`) ensuring charts can be rendered and saved cleanly on servers, CI pipelines, or local desktops without requiring a display server.
