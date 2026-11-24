"""
Report Export Module
File: src/exporter.py
Purpose: Export weather records, statistical summaries, and threshold alerts to CSV, TXT, and Markdown formats.
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.analytics import generate_summary
from src.alerts import generate_alerts

REPORTS_DIR = Path("reports")


def ensure_reports_dir(dir_path: Optional[str] = None) -> Path:
    p = Path(dir_path) if dir_path else REPORTS_DIR
    p.mkdir(parents=True, exist_ok=True)
    return p


def export_csv_report(
    records: List[Dict[str, Any]],
    summary_stats: Dict[str, Any],
    file_path: Optional[str] = None,
) -> str:
    """
    Export detailed analysis and records into a structured CSV file.
    """
    out_dir = ensure_reports_dir()
    target_path = Path(file_path) if file_path else out_dir / "analysis_report.csv"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    with open(target_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        # Section 1: Executive Summary
        writer.writerow(["=== WEATHER ANALYSIS SUMMARY ==="])
        writer.writerow(["Generated At", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow(["Total Records", summary_stats.get("record_count", len(records))])
        
        temp_data = summary_stats.get("temperature", {})
        writer.writerow(["Average Temperature (°C)", temp_data.get("average", "N/A")])
        if temp_data.get("max"):
            writer.writerow(["Max Temperature (°C)", temp_data["max"].get("value"), "Date:", temp_data["max"].get("date")])
        if temp_data.get("min"):
            writer.writerow(["Min Temperature (°C)", temp_data["min"].get("value"), "Date:", temp_data["min"].get("date")])

        rain_data = summary_stats.get("rainfall", {})
        writer.writerow(["Total Rainfall (mm)", rain_data.get("total", "N/A")])
        writer.writerow(["Average Daily Rainfall (mm)", rain_data.get("average", "N/A")])
        writer.writerow(["Rainy Days Count", rain_data.get("rainy_days", "N/A")])

        hum_data = summary_stats.get("humidity", {})
        writer.writerow(["Average Humidity (%)", hum_data.get("average", "N/A")])

        writer.writerow([])
        writer.writerow(["=== INDIVIDUAL WEATHER OBSERVATIONS ==="])
        writer.writerow(["Date", "City", "Temperature (°C)", "Rainfall (mm)", "Humidity (%)", "Wind Speed (km/h)"])

        for r in records:
            writer.writerow([
                r.get("date", ""),
                r.get("city", ""),
                r.get("temperature", ""),
                r.get("rainfall", ""),
                r.get("humidity", ""),
                r.get("wind_speed", ""),
            ])

    return str(target_path)


def export_text_report(
    records: List[Dict[str, Any]],
    summary_stats: Dict[str, Any],
    file_path: Optional[str] = None,
    alerts_list: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Export human-readable text report with clean ASCII formatting.
    """
    out_dir = ensure_reports_dir()
    target_path = Path(file_path) if file_path else out_dir / "summary_report.txt"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if alerts_list is None:
        alerts_list = generate_alerts(records)

    lines = [
        "=======================================================================",
        "                    WEATHER DATA ANALYSIS REPORT                       ",
        "                   CampusSolve Project #91 Visualizer                  ",
        "=======================================================================",
        f"Generated On  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Records : {len(records)}",
        "-----------------------------------------------------------------------",
        "1. KEY WEATHER STATISTICS",
        "-----------------------------------------------------------------------",
    ]

    temp = summary_stats.get("temperature", {})
    rain = summary_stats.get("rainfall", {})
    hum = summary_stats.get("humidity", {})
    wind = summary_stats.get("wind_speed", {})

    lines.append(f"Temperature:")
    lines.append(f"  • Mean Temperature      : {temp.get('average', 'N/A')} °C")
    if temp.get("max"):
        lines.append(f"  • Maximum Temperature   : {temp['max'].get('value')} °C ({temp['max'].get('date')} - {temp['max'].get('city')})")
    if temp.get("min"):
        lines.append(f"  • Minimum Temperature   : {temp['min'].get('value')} °C ({temp['min'].get('date')} - {temp['min'].get('city')})")
    lines.append(f"  • Temperature Trend     : {temp.get('trend', {}).get('trend', 'N/A')} (Slope: {temp.get('trend', {}).get('slope', 0.0)})")

    lines.append(f"\nRainfall & Moisture:")
    lines.append(f"  • Total Precipitation   : {rain.get('total', 0.0)} mm")
    lines.append(f"  • Daily Average         : {rain.get('average', 0.0)} mm")
    lines.append(f"  • Rainy Days (>= {rain.get('rainy_day_threshold', 0.1)}mm) : {rain.get('rainy_days', 0)}")
    lines.append(f"  • Mean Relative Humidity: {hum.get('average', 'N/A')} %")

    lines.append(f"\nWind Measurements:")
    lines.append(f"  • Average Wind Speed    : {wind.get('average', 'N/A')} km/h")
    if wind.get("max"):
        lines.append(f"  • Peak Wind Gust        : {wind['max'].get('value')} km/h ({wind['max'].get('date')} - {wind['max'].get('city')})")

    lines.append("\n-----------------------------------------------------------------------")
    lines.append("2. THRESHOLD WARNINGS AND DATA ALERTS")
    lines.append("-----------------------------------------------------------------------")
    if alerts_list:
        for idx, a in enumerate(alerts_list, start=1):
            lines.append(f"[{a.get('severity', 'ALERT')}] {idx}. {a.get('message')}")
    else:
        lines.append("No unusual weather thresholds exceeded. All readings normal.")

    lines.append("\n-----------------------------------------------------------------------")
    lines.append("3. DATASET SAMPLE PREVIEW")
    lines.append("-----------------------------------------------------------------------")
    lines.append(f"{'Date':<12} | {'City':<14} | {'Temp (°C)':<10} | {'Rain (mm)':<10} | {'Humidity':<8} | {'Wind (km/h)':<10}")
    lines.append("-" * 75)
    for r in records[:15]:
        lines.append(
            f"{str(r.get('date', '')):<12} | "
            f"{str(r.get('city', '')):<14} | "
            f"{float(r.get('temperature', 0.0)):<10.1f} | "
            f"{float(r.get('rainfall', 0.0)):<10.1f} | "
            f"{float(r.get('humidity', 0.0)):<8.0f}% | "
            f"{float(r.get('wind_speed', 0.0)):<10.1f}"
        )
    if len(records) > 15:
        lines.append(f"... and {len(records) - 15} more records.")

    lines.append("=======================================================================\n")

    content = "\n".join(lines)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    return str(target_path)


def export_markdown_report(
    records: List[Dict[str, Any]],
    summary_stats: Dict[str, Any],
    file_path: Optional[str] = None,
    alerts_list: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Export styled Markdown document with tables and highlight callouts.
    """
    out_dir = ensure_reports_dir()
    target_path = Path(file_path) if file_path else out_dir / "summary_report.md"
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if alerts_list is None:
        alerts_list = generate_alerts(records)

    temp = summary_stats.get("temperature", {})
    rain = summary_stats.get("rainfall", {})
    hum = summary_stats.get("humidity", {})
    wind = summary_stats.get("wind_speed", {})

    md = [
        "# Weather Data Analysis Report",
        "",
        "> **Project**: CampusSolve Project #91 | Weather Data Visualizer  ",
        f"> **Generated On**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`  ",
        f"> **Total Records Analyzed**: `{len(records)}`",
        "",
        "## 1. Executive Summary Statistics",
        "",
        "| Metric | Value | Reference / Date |",
        "| :--- | :--- | :--- |",
        f"| **Average Temperature** | `{temp.get('average', 'N/A')} °C` | Mean over observation window |",
        f"| **Maximum Temperature** | `{temp.get('max', {}).get('value', 'N/A')} °C` | {temp.get('max', {}).get('date', '')} ({temp.get('max', {}).get('city', '')}) |",
        f"| **Minimum Temperature** | `{temp.get('min', {}).get('value', 'N/A')} °C` | {temp.get('min', {}).get('date', '')} ({temp.get('min', {}).get('city', '')}) |",
        f"| **Temperature Trend** | **{temp.get('trend', {}).get('trend', 'N/A')}** | Slope: `{temp.get('trend', {}).get('slope', 0.0)}` |",
        f"| **Total Rainfall** | `{rain.get('total', 0.0)} mm` | Cumulative precipitation |",
        f"| **Average Daily Rainfall** | `{rain.get('average', 0.0)} mm` | Daily mean |",
        f"| **Rainy Days Count** | `{rain.get('rainy_days', 0)} days` | Threshold: >= {rain.get('rainy_day_threshold', 0.1)} mm |",
        f"| **Average Humidity** | `{hum.get('average', 'N/A')} %` | Mean relative humidity |",
        f"| **Average Wind Speed** | `{wind.get('average', 'N/A')} km/h` | Mean velocity |",
        f"| **Peak Wind Gust** | `{wind.get('max', {}).get('value', 'N/A')} km/h` | {wind.get('max', {}).get('date', '')} ({wind.get('max', {}).get('city', '')}) |",
        "",
        "## 2. Threshold Warnings & Environmental Alerts",
        "",
    ]

    if alerts_list:
        for a in alerts_list:
            icon = "⚠️" if a.get("severity") in ("WARNING", "CRITICAL") else "ℹ️"
            md.append(f"- {icon} **[{a.get('severity')}]** {a.get('message')}")
    else:
        md.append("> [!NOTE]")
        md.append("> All meteorological values are within safe and expected seasonal thresholds.")

    md.extend([
        "",
        "## 3. Data Observations Table (First 15 Entries)",
        "",
        "| Date | City | Temperature (°C) | Rainfall (mm) | Humidity (%) | Wind Speed (km/h) |",
        "| :--- | :--- | :---: | :---: | :---: | :---: |",
    ])

    for r in records[:15]:
        md.append(
            f"| {r.get('date')} | {r.get('city')} | {r.get('temperature')} | {r.get('rainfall')} | {r.get('humidity')}% | {r.get('wind_speed')} |"
        )

    if len(records) > 15:
        md.append(f"\n*... and {len(records) - 15} additional records omitted for brevity.*")

    content = "\n".join(md)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)

    return str(target_path)


def generate_report(
    records: List[Dict[str, Any]],
    report_type: str = "all",
    output_dir: str = "reports",
) -> Dict[str, str]:
    """
    Generate chosen report formats (csv, txt, md, or all) and return generated file paths.
    """
    summary_stats = generate_summary(records)
    alerts_list = generate_alerts(records)
    generated = {}

    out = ensure_reports_dir(output_dir)

    if report_type in ("csv", "all"):
        csv_file = out / "analysis_report.csv"
        export_csv_report(records, summary_stats, str(csv_file))
        generated["csv"] = str(csv_file)

    if report_type in ("txt", "all"):
        txt_file = out / "summary_report.txt"
        export_text_report(records, summary_stats, str(txt_file), alerts_list)
        generated["txt"] = str(txt_file)

    if report_type in ("md", "markdown", "all"):
        md_file = out / "summary_report.md"
        export_markdown_report(records, summary_stats, str(md_file), alerts_list)
        generated["md"] = str(md_file)

    return generated
