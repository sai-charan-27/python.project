"""
Visualization Module
File: src/visualizer.py
Purpose: Generate publication-quality weather trend charts and comparisons using Matplotlib.
Saves charts to disk and optionally displays interactive GUI windows.
"""

import os
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional

# Set writable cache directory for Matplotlib to avoid Windows permission warnings
mpl_cache = Path(tempfile.gettempdir()) / ".matplotlib_weather_cache"
mpl_cache.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(mpl_cache))

import matplotlib
# Use Agg backend by default for thread safety and non-blocking headless execution
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

CHARTS_DIR = Path("charts")


def ensure_charts_dir(dir_path: Optional[str] = None) -> Path:
    """Ensure the target charts directory exists."""
    p = Path(dir_path) if dir_path else CHARTS_DIR
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_chart(fig, file_path: str, dpi: int = 300) -> bool:
    """Safely save a matplotlib figure to file path."""
    try:
        p = Path(file_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        fig.tight_layout()
        fig.savefig(p, dpi=dpi, bbox_inches="tight")
        return True
    except Exception as e:
        print(f"Error saving chart to {file_path}: {e}")
        return False
    finally:
        plt.close(fig)


def _prepare_time_series(records: List[Dict[str, Any]]):
    """Sort and extract dates, temperatures, rainfalls, humidities, winds, and labels."""
    sorted_records = sorted(records, key=lambda x: str(x.get("date", "")))
    dates = []
    labels = []
    for r in sorted_records:
        d_str = str(r.get("date", "")).strip()
        try:
            dt = datetime.strptime(d_str, "%Y-%m-%d")
            dates.append(dt)
            labels.append(dt.strftime("%b %d"))
        except ValueError:
            labels.append(d_str)

    temps = [float(r.get("temperature", 0.0)) for r in sorted_records]
    rains = [float(r.get("rainfall", 0.0)) for r in sorted_records]
    hums = [float(r.get("humidity", 0.0)) for r in sorted_records]
    winds = [float(r.get("wind_speed", 0.0)) for r in sorted_records]
    cities = [str(r.get("city", "Unknown")) for r in sorted_records]

    return {
        "records": sorted_records,
        "dates": dates,
        "labels": labels,
        "temps": temps,
        "rains": rains,
        "hums": hums,
        "winds": winds,
        "cities": cities,
    }


def plot_temperature_trend(
    records: List[Dict[str, Any]],
    save_path: Optional[str] = None,
    city_filter: Optional[str] = None,
    show: bool = False,
) -> Optional[str]:
    """
    Generate and save a temperature line chart showing temperature changes by date.
    """
    if not records:
        print("No records to plot for temperature trend.")
        return None

    if city_filter:
        records = [r for r in records if str(r.get("city", "")).lower() == city_filter.lower()]
        if not records:
            print(f"No records found for city '{city_filter}'.")
            return None

    data = _prepare_time_series(records)
    out_dir = ensure_charts_dir()
    default_save = out_dir / "temperature_trend.png"
    target_path = Path(save_path) if save_path else default_save

    fig, ax = plt.subplots(figsize=(10, 5.5))
    x_indices = list(range(len(data["labels"])))

    ax.plot(
        x_indices,
        data["temps"],
        marker="o",
        color="#e63946",
        linewidth=2.5,
        markersize=6,
        label="Temperature (°C)",
    )

    # Highlight min and max points
    min_idx = data["temps"].index(min(data["temps"]))
    max_idx = data["temps"].index(max(data["temps"]))

    ax.scatter(min_idx, data["temps"][min_idx], color="#1d3557", s=100, zorder=5, label=f"Min: {data['temps'][min_idx]}°C")
    ax.scatter(max_idx, data["temps"][max_idx], color="#d62828", s=100, zorder=5, label=f"Max: {data['temps'][max_idx]}°C")

    # Annotations
    for idx, (x, y) in enumerate(zip(x_indices, data["temps"])):
        ax.annotate(
            f"{y:.1f}°",
            (x, y),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=8,
            color="#333333",
        )

    title_city = f" - {city_filter.title()}" if city_filter else f" ({records[0].get('city', 'Dataset')})"
    ax.set_title(f"Temperature Trend Over Time{title_city}", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Date", fontsize=11, fontweight="semibold")
    ax.set_ylabel("Temperature (°C)", fontsize=11, fontweight="semibold")
    ax.set_xticks(x_indices)
    ax.set_xticklabels(data["labels"], rotation=35, ha="right", fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="best", framealpha=0.9)

    save_chart(fig, str(target_path))
    if show:
        try:
            plt.show()
        except Exception:
            pass

    return str(target_path)


def plot_rainfall_trend(
    records: List[Dict[str, Any]],
    save_path: Optional[str] = None,
    city_filter: Optional[str] = None,
    show: bool = False,
) -> Optional[str]:
    """
    Generate and save a rainfall bar chart showing daily rainfall levels.
    """
    if not records:
        print("No records to plot for rainfall trend.")
        return None

    if city_filter:
        records = [r for r in records if str(r.get("city", "")).lower() == city_filter.lower()]
        if not records:
            print(f"No records found for city '{city_filter}'.")
            return None

    data = _prepare_time_series(records)
    out_dir = ensure_charts_dir()
    default_save = out_dir / "rainfall_trend.png"
    target_path = Path(save_path) if save_path else default_save

    fig, ax = plt.subplots(figsize=(10, 5.5))
    x_indices = list(range(len(data["labels"])))

    # Color code bars based on intensity
    colors = []
    for r in data["rains"]:
        if r == 0:
            colors.append("#a8dadc")
        elif r < 5.0:
            colors.append("#457b9d")
        elif r < 15.0:
            colors.append("#1d3557")
        else:
            colors.append("#6a0dad")

    bars = ax.bar(x_indices, data["rains"], color=colors, edgecolor="#1d3557", width=0.55, label="Rainfall (mm)")

    # Value labels on top of bars
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.annotate(
                f"{h:.1f}",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold",
            )

    # Average rainfall line
    avg_rain = sum(data["rains"]) / len(data["rains"]) if data["rains"] else 0.0
    ax.axhline(avg_rain, color="#e63946", linestyle=":", linewidth=1.8, label=f"Mean Rainfall ({avg_rain:.1f} mm)")

    title_city = f" - {city_filter.title()}" if city_filter else f" ({records[0].get('city', 'Dataset')})"
    ax.set_title(f"Daily Rainfall Levels{title_city}", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Date", fontsize=11, fontweight="semibold")
    ax.set_ylabel("Rainfall (mm)", fontsize=11, fontweight="semibold")
    ax.set_xticks(x_indices)
    ax.set_xticklabels(data["labels"], rotation=35, ha="right", fontsize=9)
    ax.grid(True, axis="y", linestyle="--", alpha=0.6)
    ax.legend(loc="upper right", framealpha=0.9)

    save_chart(fig, str(target_path))
    if show:
        try:
            plt.show()
        except Exception:
            pass

    return str(target_path)


def plot_humidity_trend(
    records: List[Dict[str, Any]],
    save_path: Optional[str] = None,
    show: bool = False,
) -> Optional[str]:
    """
    Generate and save a humidity trend chart showing humidity percentage changes.
    """
    if not records:
        return None

    data = _prepare_time_series(records)
    out_dir = ensure_charts_dir()
    default_save = out_dir / "humidity_trend.png"
    target_path = Path(save_path) if save_path else default_save

    fig, ax = plt.subplots(figsize=(10, 5.2))
    x_indices = list(range(len(data["labels"])))

    ax.plot(
        x_indices,
        data["hums"],
        marker="s",
        color="#2a9d8f",
        linewidth=2.2,
        label="Relative Humidity (%)",
    )
    ax.fill_between(x_indices, data["hums"], color="#2a9d8f", alpha=0.15)

    ax.set_ylim(0, 105)
    ax.set_title("Relative Humidity Trend", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Date", fontsize=11, fontweight="semibold")
    ax.set_ylabel("Humidity (%)", fontsize=11, fontweight="semibold")
    ax.set_xticks(x_indices)
    ax.set_xticklabels(data["labels"], rotation=35, ha="right", fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="best")

    save_chart(fig, str(target_path))
    if show:
        try:
            plt.show()
        except Exception:
            pass

    return str(target_path)


def plot_weather_comparison(
    records: List[Dict[str, Any]],
    save_path: Optional[str] = None,
    show: bool = False,
) -> Optional[str]:
    """
    Generate weather comparison chart across cities or multi-variables.
    """
    if not records:
        return None

    out_dir = ensure_charts_dir()
    default_save = out_dir / "weather_comparison.png"
    target_path = Path(save_path) if save_path else default_save

    # Group by city
    cities_map: Dict[str, Dict[str, List[float]]] = {}
    for r in records:
        c = str(r.get("city", "Unknown")).title()
        if c not in cities_map:
            cities_map[c] = {"temps": [], "rains": [], "hums": []}
        cities_map[c]["temps"].append(float(r.get("temperature", 0.0)))
        cities_map[c]["rains"].append(float(r.get("rainfall", 0.0)))
        cities_map[c]["hums"].append(float(r.get("humidity", 0.0)))

    city_names = list(cities_map.keys())
    if len(city_names) > 1:
        # Compare cities side-by-side
        avg_temps = [sum(cities_map[c]["temps"]) / len(cities_map[c]["temps"]) for c in city_names]
        total_rains = [sum(cities_map[c]["rains"]) for c in city_names]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.bar(city_names, avg_temps, color=["#e76f51", "#2a9d8f", "#457b9d"][:len(city_names)], edgecolor="#333")
        ax1.set_title("Average Temperature by City (°C)", fontweight="bold")
        ax1.set_ylabel("Temp (°C)")
        ax1.grid(True, axis="y", linestyle="--", alpha=0.5)

        ax2.bar(city_names, total_rains, color=["#1d3557", "#0077b6", "#90e0ef"][:len(city_names)], edgecolor="#333")
        ax2.set_title("Total Rainfall by City (mm)", fontweight="bold")
        ax2.set_ylabel("Rainfall (mm)")
        ax2.grid(True, axis="y", linestyle="--", alpha=0.5)
    else:
        # Single city: Dual axis chart of Temperature vs Rainfall
        data = _prepare_time_series(records)
        x_indices = list(range(len(data["labels"])))

        fig, ax1 = plt.subplots(figsize=(10, 5.5))
        ax2 = ax1.twinx()

        line = ax1.plot(x_indices, data["temps"], color="#e63946", marker="o", linewidth=2.5, label="Temperature (°C)")
        bars = ax2.bar(x_indices, data["rains"], color="#457b9d", alpha=0.45, width=0.5, label="Rainfall (mm)")

        ax1.set_xlabel("Date", fontweight="semibold")
        ax1.set_ylabel("Temperature (°C)", color="#e63946", fontweight="semibold")
        ax2.set_ylabel("Rainfall (mm)", color="#457b9d", fontweight="semibold")
        ax1.set_xticks(x_indices)
        ax1.set_xticklabels(data["labels"], rotation=35, ha="right", fontsize=9)
        ax1.set_title(f"Weather Comparison: Temperature vs Rainfall ({city_names[0]})", fontweight="bold", pad=15)
        ax1.grid(True, linestyle="--", alpha=0.5)

    save_chart(fig, str(target_path))
    if show:
        try:
            plt.show()
        except Exception:
            pass

    return str(target_path)


def plot_combined_dashboard(
    records: List[Dict[str, Any]],
    save_path: Optional[str] = None,
    show: bool = False,
) -> Optional[str]:
    """
    Generate a 4-panel comprehensive weather dashboard.
    """
    if not records:
        return None

    data = _prepare_time_series(records)
    out_dir = ensure_charts_dir()
    default_save = out_dir / "weather_dashboard.png"
    target_path = Path(save_path) if save_path else default_save

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 9))
    x_indices = list(range(len(data["labels"])))

    # Panel 1: Temperature
    ax1.plot(x_indices, data["temps"], marker="o", color="#e63946", linewidth=2)
    ax1.set_title("Temperature Trend (°C)", fontweight="bold")
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(data["labels"], rotation=35, ha="right", fontsize=8)
    ax1.grid(True, linestyle="--", alpha=0.5)

    # Panel 2: Rainfall
    ax2.bar(x_indices, data["rains"], color="#457b9d", edgecolor="#1d3557")
    ax2.set_title("Daily Rainfall (mm)", fontweight="bold")
    ax2.set_xticks(x_indices)
    ax2.set_xticklabels(data["labels"], rotation=35, ha="right", fontsize=8)
    ax2.grid(True, axis="y", linestyle="--", alpha=0.5)

    # Panel 3: Humidity
    ax3.plot(x_indices, data["hums"], marker="s", color="#2a9d8f", linewidth=2)
    ax3.set_title("Relative Humidity (%)", fontweight="bold")
    ax3.set_xticks(x_indices)
    ax3.set_xticklabels(data["labels"], rotation=35, ha="right", fontsize=8)
    ax3.grid(True, linestyle="--", alpha=0.5)

    # Panel 4: Wind Speed
    ax4.plot(x_indices, data["winds"], marker="^", color="#f4a261", linewidth=2)
    ax4.set_title("Wind Speed (km/h)", fontweight="bold")
    ax4.set_xticks(x_indices)
    ax4.set_xticklabels(data["labels"], rotation=35, ha="right", fontsize=8)
    ax4.grid(True, linestyle="--", alpha=0.5)

    fig.suptitle(f"Weather Analytics Dashboard - {records[0].get('city', 'Dataset')}", fontsize=16, fontweight="bold")
    save_chart(fig, str(target_path))
    if show:
        try:
            plt.show()
        except Exception:
            pass

    return str(target_path)
