"""
Main Application Module
File: main.py
Purpose: The primary entry point for the Weather Data Visualizer application.
CampusSolve Project #91
"""

import sys
import os
import tempfile
from pathlib import Path
from typing import Dict, Any

# Ensure Matplotlib uses a writable temp cache directory on Windows
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / ".matplotlib_weather_cache"))

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.menu import display_welcome_screen, display_menu, handle_menu_selection
from src.storage import load_from_csv, load_from_json, save_to_csv, save_to_json
from src.data_loader import load_sample_data
from src.validator import DEFAULT_CONFIG
from src.input_handler import get_integer_input


def initialize_application() -> Dict[str, Any]:
    """
    Initialize runtime environment, directory structures, and preload saved weather records.
    """
    # Create required standard directories
    for d in ["data", "charts", "reports", "docs"]:
        (PROJECT_ROOT / d).mkdir(parents=True, exist_ok=True)

    state: Dict[str, Any] = {
        "records": [],
        "config": DEFAULT_CONFIG.copy(),
        "modified": False,
    }

    # Attempt to load persistent data
    csv_storage = PROJECT_ROOT / "data" / "weather_data.csv"
    json_storage = PROJECT_ROOT / "data" / "weather_data.json"
    sample_csv = PROJECT_ROOT / "data" / "sample_weather.csv"

    if csv_storage.exists():
        records, msg = load_from_csv(str(csv_storage))
        if records:
            state["records"] = records
            print(f"[*] Initialized: Loaded {len(records)} existing records from '{csv_storage.name}'.")
    elif json_storage.exists():
        records, msg = load_from_json(str(json_storage))
        if records:
            state["records"] = records
            print(f"[*] Initialized: Loaded {len(records)} existing records from '{json_storage.name}'.")
    elif sample_csv.exists():
        records, _, _ = load_sample_data(str(sample_csv))
        if records:
            state["records"] = records
            print(f"[*] Initialized: Preloaded {len(records)} records from sample dataset.")

    return state


def shutdown_application(state: Dict[str, Any]):
    """
    Perform graceful shutdown: persist records to disk and notify user.
    """
    records = state.get("records", [])
    if records:
        csv_file = PROJECT_ROOT / "data" / "weather_data.csv"
        json_file = PROJECT_ROOT / "data" / "weather_data.json"
        save_to_csv(records, str(csv_file))
        save_to_json(records, str(json_file))
        print("[✓] Session state auto-saved to CSV and JSON.")

    print("\nThank you for using Weather Data Visualizer. Goodbye!")


def main():
    """
    Application main execution loop.
    """
    display_welcome_screen()
    state = initialize_application()

    is_running = True
    while is_running:
        try:
            display_menu(len(state.get("records", [])))
            choice = get_integer_input("Select an option (0-14)", min_val=0, max_val=14)
            is_running = handle_menu_selection(choice, state)
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Operation interrupted by user.")
            break
        except Exception as e:
            print(f"\n[!] An unexpected error occurred: {e}")
            print("The application recovered safely and remains active.")

    shutdown_application(state)


if __name__ == "__main__":
    main()
