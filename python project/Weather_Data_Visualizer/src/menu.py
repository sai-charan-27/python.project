"""
Interactive Menu Module
File: src/menu.py
Purpose: Provide interactive terminal interface, menus, table formatting, and command routing.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.input_handler import (
    get_integer_input,
    get_float_input,
    get_date_input,
    get_text_input,
    confirm,
)
from src.validator import validate_record, DEFAULT_CONFIG
from src.data_loader import load_sample_data, load_csv_file
from src.data_processor import clean_data, sort_by_date, prepare_analysis_data
from src.storage import save_to_csv, save_to_json, load_from_csv, load_from_json, backup_data, restore_data
from src.search import search_by_city, search_by_date, filter_by_temperature, filter_by_rainfall, search_by_keyword
from src.analytics import generate_summary
from src.visualizer import (
    plot_temperature_trend,
    plot_rainfall_trend,
    plot_humidity_trend,
    plot_weather_comparison,
    plot_combined_dashboard,
)
from src.exporter import export_csv_report, export_text_report, export_markdown_report, generate_report
from src.alerts import generate_alerts


def display_welcome_screen():
    """Display modern stylized startup banner."""
    print(r"""
========================================================================
 **********************************************************************
 *                      WEATHER DATA VISUALIZER                       *
 *              Data & Visualization | CampusSolve Project #91        *
 *                  Python • CSV • JSON • Matplotlib                  *
 **********************************************************************
========================================================================
   Analyze weather statistics, visualize temperature and rainfall
   trends, and export reports without relying on complicated services.
------------------------------------------------------------------------
""")


def display_menu(record_count: int = 0):
    """Display the main numbered CLI menu."""
    print("\n" + "=" * 50)
    print(f" MAIN MENU  [Current Loaded Records: {record_count}]")
    print("=" * 50)
    print(" 1.  Load sample weather data")
    print(" 2.  Import external weather CSV file")
    print(" 3.  View all weather records")
    print(" 4.  Add a new weather record (with validation)")
    print(" 5.  Search and filter weather records")
    print(" 6.  Display statistical analytics")
    print(" 7.  Generate & view temperature charts")
    print(" 8.  Generate & view rainfall charts")
    print(" 9.  Generate & view humidity & comparison charts")
    print(" 10. Export reports (CSV, TXT, Markdown)")
    print(" 11. View weather threshold warnings & data alerts")
    print(" 12. Save records to disk (CSV & JSON)")
    print(" 13. Backup & restore data")
    print(" 14. Configure validation & alert thresholds")
    print(" 0.  Exit Application")
    print("-" * 50)


def display_records(records: List[Dict[str, Any]], page_size: int = 15):
    """Format and display weather records in a neat ASCII table with pagination."""
    if not records:
        print("\n[!] No records found to display.")
        return

    total = len(records)
    print(f"\nDisplaying {total} weather record(s):")
    header = f"{'#':<4} | {'Date':<11} | {'City':<14} | {'Temp (°C)':<10} | {'Rain (mm)':<10} | {'Humidity':<9} | {'Wind (km/h)':<11}"
    separator = "-" * len(header)

    offset = 0
    while offset < total:
        print("\n" + separator)
        print(header)
        print(separator)

        page_records = records[offset : offset + page_size]
        for idx, r in enumerate(page_records, start=offset + 1):
            print(
                f"{idx:<4} | "
                f"{str(r.get('date', '')):<11} | "
                f"{str(r.get('city', '')):<14} | "
                f"{float(r.get('temperature', 0.0)):<10.1f} | "
                f"{float(r.get('rainfall', 0.0)):<10.1f} | "
                f"{float(r.get('humidity', 0.0)):<8.1f}% | "
                f"{float(r.get('wind_speed', 0.0)):<11.1f}"
            )
        print(separator)

        offset += page_size
        if offset < total:
            cont = confirm(f"Showing {offset} of {total} records. Show next {min(page_size, total - offset)} records?", default=True)
            if not cont:
                break


def handle_menu_selection(choice: int, state: Dict[str, Any]) -> bool:
    """
    Dispatch menu choice to appropriate module function.
    Returns: True to continue running, False to shut down.
    """
    records = state.get("records", [])
    config = state.get("config", DEFAULT_CONFIG)

    if choice == 0:
        return False

    elif choice == 1:
        # Load sample data
        print("\n[*] Loading sample weather dataset...")
        valid, invalid, errs = load_sample_data(config=config)
        if errs:
            print(f"[!] Error loading sample data: {errs}")
        else:
            state["records"] = valid
            print(f"[✓] Successfully loaded {len(valid)} records from sample dataset!")
            if invalid:
                print(f"[!] Detected {len(invalid)} malformed row(s) in sample file.")

    elif choice == 2:
        # Import CSV
        csv_path = get_text_input("\nEnter CSV file path to import (e.g. data/sample_weather.csv): ")
        print(f"[*] Importing '{csv_path}'...")
        valid, invalid, errs = load_csv_file(csv_path, config=config)
        if errs:
            print(f"[!] Import failed:")
            for e in errs:
                print(f"    - {e}")
        else:
            if confirm(f"Loaded {len(valid)} valid records. Replace current records? (Select 'No' to append)", default=False):
                state["records"] = valid
            else:
                state["records"] = clean_data(state["records"] + valid)
            print(f"[✓] Success! Total records in memory: {len(state['records'])}")
            if invalid:
                print(f"[!] Note: {len(invalid)} row(s) failed validation and were skipped.")

    elif choice == 3:
        # View records
        display_records(records)

    elif choice == 4:
        # Add new record
        print("\n=== ADD NEW WEATHER RECORD ===")
        date_val = get_date_input("Enter Date (YYYY-MM-DD)")
        city_val = get_text_input("Enter City name")
        
        min_t = config.get("min_temperature", -50.0)
        max_t = config.get("max_temperature", 60.0)
        temp_val = get_float_input(f"Enter Temperature in °C (Valid range: {min_t} to {max_t})", min_val=min_t, max_val=max_t)

        min_r = config.get("min_rainfall", 0.0)
        max_r = config.get("max_rainfall", 1000.0)
        rain_val = get_float_input(f"Enter Rainfall in mm (Valid range: >= {min_r})", min_val=min_r, max_val=max_r)

        min_h = config.get("min_humidity", 0.0)
        max_h = config.get("max_humidity", 100.0)
        hum_val = get_float_input(f"Enter Relative Humidity in % (0 - 100)", min_val=min_h, max_val=max_h)

        min_w = config.get("min_wind_speed", 0.0)
        max_w = config.get("max_wind_speed", 250.0)
        wind_val = get_float_input(f"Enter Wind Speed in km/h (Valid range: >= {min_w})", min_val=min_w, max_val=max_w)

        new_record = {
            "date": date_val,
            "city": city_val.title(),
            "temperature": round(temp_val, 2),
            "rainfall": round(rain_val, 2),
            "humidity": round(hum_val, 1),
            "wind_speed": round(wind_val, 2),
        }

        # Double validate with validator module
        is_valid, errors = validate_record(new_record, config)
        if is_valid:
            state["records"].append(new_record)
            state["records"] = sort_by_date(state["records"])
            print(f"\n[✓] Record for {new_record['city']} on {new_record['date']} successfully validated and added!")
        else:
            print(f"\n[!] Record validation failed:")
            for err in errors:
                print(f"    - {err}")

    elif choice == 5:
        # Search & Filter
        if not records:
            print("[!] No records available to search. Please load data first.")
            return True

        print("\n--- SEARCH AND FILTER OPTIONS ---")
        print("1. Search by City")
        print("2. Search by Date or Date Range")
        print("3. Filter by Temperature Range")
        print("4. Filter by Rainfall Range")
        print("5. General Keyword Search")
        sub_choice = get_integer_input("Select filter option (1-5)", min_val=1, max_val=5)

        if sub_choice == 1:
            city_query = get_text_input("Enter city name to search")
            matched = search_by_city(records, city_query)
            display_records(matched)
        elif sub_choice == 2:
            print("1. Single Date  2. Date Range")
            sub_d = get_integer_input("Choice", min_val=1, max_val=2)
            if sub_d == 1:
                t_date = get_date_input("Target Date")
                matched = search_by_date(records, target_date=t_date)
            else:
                s_date = get_date_input("Start Date")
                e_date = get_date_input("End Date")
                matched = search_by_date(records, start_date=s_date, end_date=e_date)
            display_records(matched)
        elif sub_choice == 3:
            min_t = get_float_input("Minimum Temperature (°C) [press Enter to skip]", default=-999.0)
            max_t = get_float_input("Maximum Temperature (°C) [press Enter to skip]", default=999.0)
            min_arg = min_t if min_t != -999.0 else None
            max_arg = max_t if max_t != 999.0 else None
            matched = filter_by_temperature(records, min_arg, max_arg)
            display_records(matched)
        elif sub_choice == 4:
            min_r = get_float_input("Minimum Rainfall (mm) [press Enter to skip]", default=-1.0)
            max_r = get_float_input("Maximum Rainfall (mm) [press Enter to skip]", default=-1.0)
            min_arg = min_r if min_r != -1.0 else None
            max_arg = max_r if max_r != -1.0 else None
            matched = filter_by_rainfall(records, min_arg, max_arg)
            display_records(matched)
        elif sub_choice == 5:
            kw = get_text_input("Enter keyword")
            matched = search_by_keyword(records, kw)
            display_records(matched)

    elif choice == 6:
        # Analytics
        if not records:
            print("[!] No records available to analyze. Please load data first.")
            return True

        summary = generate_summary(records)
        print("\n" + "=" * 55)
        print("          WEATHER STATISTICAL ANALYTICS REPORT          ")
        print("=" * 55)
        print(f"Total Observations : {summary['record_count']}")
        print(f"Observation Window : {summary['date_range']['start']} to {summary['date_range']['end']}")
        print("-" * 55)

        t = summary["temperature"]
        print(f"TEMPERATURE METRICS:")
        print(f"  • Average (Mean) : {t['average']} °C")
        if t.get("max"):
            print(f"  • Maximum Record : {t['max']['value']} °C ({t['max']['date']} - {t['max']['city']})")
        if t.get("min"):
            print(f"  • Minimum Record : {t['min']['value']} °C ({t['min']['date']} - {t['min']['city']})")
        print(f"  • Overall Trend  : {t['trend']['trend']} (Slope: {t['trend']['slope']})")

        r = summary["rainfall"]
        print(f"\nPRECIPITATION & RAINFALL:")
        print(f"  • Cumulative Total : {r['total']} mm")
        print(f"  • Daily Average    : {r['average']} mm")
        print(f"  • Rainy Days Count : {r['rainy_days']} days (Threshold >= {r['rainy_day_threshold']} mm)")
        print(f"  • Rainfall Trend   : {r['trend']['trend']}")

        h = summary["humidity"]
        print(f"\nHUMIDITY:")
        print(f"  • Average Humidity : {h['average']} %")

        w = summary["wind_speed"]
        print(f"\nWIND STATISTICS:")
        print(f"  • Mean Wind Speed  : {w['average']} km/h")
        if w.get("max"):
            print(f"  • Peak Wind Gust   : {w['max']['value']} km/h ({w['max']['date']} - {w['max']['city']})")
        print("=" * 55)

    elif choice == 7:
        # Temperature chart
        if not records:
            print("[!] Please load weather data before generating charts.")
            return True
        print("[*] Generating temperature line chart...")
        saved_file = plot_temperature_trend(records)
        print(f"[✓] Temperature trend chart saved to: {saved_file}")

    elif choice == 8:
        # Rainfall chart
        if not records:
            print("[!] Please load weather data before generating charts.")
            return True
        print("[*] Generating rainfall bar chart...")
        saved_file = plot_rainfall_trend(records)
        print(f"[✓] Rainfall trend chart saved to: {saved_file}")

    elif choice == 9:
        # Humidity & comparison
        if not records:
            print("[!] Please load weather data before generating charts.")
            return True
        print("[*] Generating humidity and multi-variable comparison charts...")
        hum_file = plot_humidity_trend(records)
        comp_file = plot_weather_comparison(records)
        dash_file = plot_combined_dashboard(records)
        print(f"[✓] Humidity chart saved to: {hum_file}")
        print(f"[✓] Comparison chart saved to: {comp_file}")
        print(f"[✓] Complete dashboard saved to: {dash_file}")

    elif choice == 10:
        # Export reports
        if not records:
            print("[!] Please load weather data before exporting reports.")
            return True
        print("\n[*] Exporting comprehensive reports...")
        results = generate_report(records, report_type="all")
        print("[✓] Reports generated successfully:")
        for fmt, path in results.items():
            print(f"    • {fmt.upper():<4} Report: {path}")

    elif choice == 11:
        # View Warnings / Alerts
        if not records:
            print("[!] Please load weather data before checking threshold alerts.")
            return True
        alerts = generate_alerts(records)
        print("\n" + "=" * 60)
        print("         WEATHER THRESHOLD WARNINGS & ADVISORIES        ")
        print(" Notice: Based on configurable dataset thresholds.       ")
        print("=" * 60)
        if not alerts:
            print("[✓] No unusual weather conditions or anomalies detected.")
        else:
            for idx, a in enumerate(alerts, start=1):
                sev = a.get("severity", "WARNING")
                print(f"[{sev}] {idx}. {a.get('message')}")
        print("=" * 60)

    elif choice == 12:
        # Save to disk
        if not records:
            print("[!] No records in memory to save.")
            return True
        csv_path = "data/weather_data.csv"
        json_path = "data/weather_data.json"
        ok_csv, msg_csv = save_to_csv(records, csv_path)
        ok_json, msg_json = save_to_json(records, json_path)
        if ok_csv:
            print(f"[✓] {msg_csv}")
        else:
            print(f"[!] {msg_csv}")
        if ok_json:
            print(f"[✓] {msg_json}")
        else:
            print(f"[!] {msg_json}")

    elif choice == 13:
        # Backup & restore
        print("\n--- BACKUP & RESTORE DATA ---")
        print("1. Create Backup of current weather data")
        print("2. Restore Data from a Backup file")
        sub_br = get_integer_input("Select option (1-2)", min_val=1, max_val=2)
        if sub_br == 1:
            src = "data/weather_data.csv"
            ok, res = backup_data(src)
            if ok:
                print(f"[✓] Backup successfully created at: {res}")
            else:
                print(f"[!] Backup failed: {res}")
        elif sub_br == 2:
            bk_file = get_text_input("Enter path to backup file to restore: ")
            ok, res = restore_data(bk_file, "data/weather_data.csv")
            if ok:
                loaded, _ = load_from_csv("data/weather_data.csv")
                state["records"] = loaded
                print(f"[✓] {res}")
            else:
                print(f"[!] {res}")

    elif choice == 14:
        # Configure thresholds
        print("\n--- CONFIGURE THRESHOLDS ---")
        print(f"Current Config:")
        print(f"  • Min Temperature : {config.get('min_temperature')} °C")
        print(f"  • Max Temperature : {config.get('max_temperature')} °C")
        print(f"  • Max Wind Speed  : {config.get('max_wind_speed')} km/h")
        print(f"  • Max Rainfall    : {config.get('max_rainfall')} mm")
        if confirm("Do you want to adjust validation thresholds?", default=False):
            config["min_temperature"] = get_float_input("Enter new Min Temperature (°C)", default=config.get("min_temperature"))
            config["max_temperature"] = get_float_input("Enter new Max Temperature (°C)", default=config.get("max_temperature"))
            config["max_wind_speed"] = get_float_input("Enter new Max Wind Speed (km/h)", default=config.get("max_wind_speed"))
            config["max_rainfall"] = get_float_input("Enter new Max Rainfall (mm)", default=config.get("max_rainfall"))
            print("[✓] Thresholds updated successfully!")

    return True
