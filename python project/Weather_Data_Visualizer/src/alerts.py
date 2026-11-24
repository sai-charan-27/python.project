"""
Threshold Alerts Module
File: src/alerts.py
Purpose: Identify unusual values, exceedance of configurable thresholds, and potential data anomalies.
Notice: These are data-based statistical threshold alerts, not official meteorology forecasts or emergency warnings.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

DEFAULT_ALERT_THRESHOLDS = {
    "high_temperature": 35.0,     # °C - Heat warning threshold
    "low_temperature": 5.0,       # °C - Cold/frost warning threshold
    "heavy_rainfall": 10.0,       # mm - Heavy rain threshold
    "extreme_rainfall": 40.0,     # mm - Torrential rain threshold
    "high_humidity": 80.0,        # % - Muggy / high moisture
    "low_humidity": 25.0,         # % - Arid / high fire danger
    "high_wind": 25.0,            # km/h - Strong wind threshold
    "max_daily_temp_delta": 8.0,  # °C - Sudden jump between consecutive days
}


def check_temperature_threshold(
    records: List[Dict[str, Any]],
    high_temp: Optional[float] = None,
    low_temp: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """Check for high heat or extreme cold exceedances."""
    if high_temp is None:
        high_temp = DEFAULT_ALERT_THRESHOLDS["high_temperature"]
    if low_temp is None:
        low_temp = DEFAULT_ALERT_THRESHOLDS["low_temperature"]

    alerts = []
    for r in records:
        try:
            t = float(r.get("temperature", 0.0))
            if t >= high_temp:
                alerts.append({
                    "type": "HIGH_TEMPERATURE",
                    "severity": "WARNING",
                    "date": r.get("date"),
                    "city": r.get("city"),
                    "value": t,
                    "threshold": high_temp,
                    "message": f"High Temperature Alert: {t}°C on {r.get('date')} in {r.get('city')} (Threshold >= {high_temp}°C)",
                })
            elif t <= low_temp:
                alerts.append({
                    "type": "LOW_TEMPERATURE",
                    "severity": "ADVISORY",
                    "date": r.get("date"),
                    "city": r.get("city"),
                    "value": t,
                    "threshold": low_temp,
                    "message": f"Low Temperature / Frost Advisory: {t}°C on {r.get('date')} in {r.get('city')} (Threshold <= {low_temp}°C)",
                })
        except (ValueError, TypeError):
            continue
    return alerts


def check_rainfall_threshold(
    records: List[Dict[str, Any]],
    heavy_rain: Optional[float] = None,
    extreme_rain: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """Check for heavy and extreme rainfall exceedances."""
    if heavy_rain is None:
        heavy_rain = DEFAULT_ALERT_THRESHOLDS["heavy_rainfall"]
    if extreme_rain is None:
        extreme_rain = DEFAULT_ALERT_THRESHOLDS["extreme_rainfall"]

    alerts = []
    for r in records:
        try:
            rain = float(r.get("rainfall", 0.0))
            if rain >= extreme_rain:
                alerts.append({
                    "type": "EXTREME_RAINFALL",
                    "severity": "CRITICAL",
                    "date": r.get("date"),
                    "city": r.get("city"),
                    "value": rain,
                    "threshold": extreme_rain,
                    "message": f"Extreme Rainfall Warning: {rain} mm on {r.get('date')} in {r.get('city')} (Threshold >= {extreme_rain} mm)",
                })
            elif rain >= heavy_rain:
                alerts.append({
                    "type": "HEAVY_RAINFALL",
                    "severity": "WARNING",
                    "date": r.get("date"),
                    "city": r.get("city"),
                    "value": rain,
                    "threshold": heavy_rain,
                    "message": f"Heavy Rainfall Alert: {rain} mm on {r.get('date')} in {r.get('city')} (Threshold >= {heavy_rain} mm)",
                })
        except (ValueError, TypeError):
            continue
    return alerts


def check_humidity_threshold(
    records: List[Dict[str, Any]],
    high_humidity: Optional[float] = None,
    low_humidity: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """Check for extreme humidity conditions."""
    if high_humidity is None:
        high_humidity = DEFAULT_ALERT_THRESHOLDS["high_humidity"]
    if low_humidity is None:
        low_humidity = DEFAULT_ALERT_THRESHOLDS["low_humidity"]

    alerts = []
    for r in records:
        try:
            h = float(r.get("humidity", 0.0))
            if h >= high_humidity:
                alerts.append({
                    "type": "HIGH_HUMIDITY",
                    "severity": "ADVISORY",
                    "date": r.get("date"),
                    "city": r.get("city"),
                    "value": h,
                    "threshold": high_humidity,
                    "message": f"High Humidity Advisory: {h}% on {r.get('date')} in {r.get('city')} (Threshold >= {high_humidity}%)",
                })
            elif h <= low_humidity:
                alerts.append({
                    "type": "LOW_HUMIDITY",
                    "severity": "ADVISORY",
                    "date": r.get("date"),
                    "city": r.get("city"),
                    "value": h,
                    "threshold": low_humidity,
                    "message": f"Low Humidity Advisory (Arid): {h}% on {r.get('date')} in {r.get('city')} (Threshold <= {low_humidity}%)",
                })
        except (ValueError, TypeError):
            continue
    return alerts


def check_wind_threshold(
    records: List[Dict[str, Any]],
    high_wind: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """Check for high wind conditions."""
    if high_wind is None:
        high_wind = DEFAULT_ALERT_THRESHOLDS["high_wind"]

    alerts = []
    for r in records:
        try:
            w = float(r.get("wind_speed", 0.0))
            if w >= high_wind:
                alerts.append({
                    "type": "HIGH_WIND",
                    "severity": "WARNING",
                    "date": r.get("date"),
                    "city": r.get("city"),
                    "value": w,
                    "threshold": high_wind,
                    "message": f"High Wind Alert: {w} km/h on {r.get('date')} in {r.get('city')} (Threshold >= {high_wind} km/h)",
                })
        except (ValueError, TypeError):
            continue
    return alerts


def check_data_anomalies(
    records: List[Dict[str, Any]],
    max_jump: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """
    Check for rapid day-over-day temperature swings or missing sequential dates.
    """
    if max_jump is None:
        max_jump = DEFAULT_ALERT_THRESHOLDS["max_daily_temp_delta"]

    alerts = []
    # Sort chronologically
    sorted_records = sorted(records, key=lambda x: str(x.get("date", "")))

    for i in range(1, len(sorted_records)):
        prev = sorted_records[i - 1]
        curr = sorted_records[i]

        # Check consecutive day jump if same city
        if prev.get("city") == curr.get("city"):
            try:
                p_temp = float(prev.get("temperature", 0.0))
                c_temp = float(curr.get("temperature", 0.0))
                delta = abs(c_temp - p_temp)
                if delta >= max_jump:
                    alerts.append({
                        "type": "TEMPERATURE_ANOMALY",
                        "severity": "INFO",
                        "date": curr.get("date"),
                        "city": curr.get("city"),
                        "value": round(delta, 2),
                        "threshold": max_jump,
                        "message": (
                            f"Rapid Temperature Shift: {delta:.1f}°C difference between "
                            f"{prev.get('date')} ({p_temp}°C) and {curr.get('date')} ({c_temp}°C) in {curr.get('city')}"
                        ),
                    })
            except (ValueError, TypeError):
                pass

    return alerts


def generate_alerts(
    records: List[Dict[str, Any]],
    thresholds: Optional[Dict[str, float]] = None,
) -> List[Dict[str, Any]]:
    """
    Compile all threshold warnings, environmental advisories, and data anomalies into a unified list.
    """
    cfg = DEFAULT_ALERT_THRESHOLDS.copy()
    if thresholds:
        cfg.update(thresholds)

    all_alerts = []
    all_alerts.extend(check_temperature_threshold(records, cfg["high_temperature"], cfg["low_temperature"]))
    all_alerts.extend(check_rainfall_threshold(records, cfg["heavy_rainfall"], cfg["extreme_rainfall"]))
    all_alerts.extend(check_humidity_threshold(records, cfg["high_humidity"], cfg["low_humidity"]))
    all_alerts.extend(check_wind_threshold(records, cfg["high_wind"]))
    all_alerts.extend(check_data_anomalies(records, cfg["max_daily_temp_delta"]))

    # Sort alerts chronologically
    all_alerts.sort(key=lambda a: str(a.get("date", "")))
    return all_alerts
