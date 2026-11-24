"""
Analytics Module
File: src/analytics.py
Purpose: Calculate statistical metrics, trends, and summary insights from weather records.
"""

import statistics
from typing import List, Dict, Any, Optional


def calculate_average_temperature(records: List[Dict[str, Any]]) -> Optional[float]:
    """Calculate mean temperature across records."""
    if not records:
        return None
    temps = [float(r["temperature"]) for r in records if "temperature" in r]
    return round(statistics.mean(temps), 2) if temps else None


def calculate_max_temperature(records: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Find maximum temperature and the corresponding record."""
    if not records:
        return None
    highest = max(records, key=lambda r: float(r.get("temperature", float("-inf"))))
    return {
        "value": round(float(highest["temperature"]), 2),
        "date": highest.get("date"),
        "city": highest.get("city"),
    }


def calculate_min_temperature(records: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Find minimum temperature and the corresponding record."""
    if not records:
        return None
    lowest = min(records, key=lambda r: float(r.get("temperature", float("inf"))))
    return {
        "value": round(float(lowest["temperature"]), 2),
        "date": lowest.get("date"),
        "city": lowest.get("city"),
    }


def calculate_total_rainfall(records: List[Dict[str, Any]]) -> float:
    """Calculate sum of rainfall in mm across all records."""
    if not records:
        return 0.0
    return round(sum(float(r.get("rainfall", 0.0)) for r in records), 2)


def calculate_average_rainfall(records: List[Dict[str, Any]]) -> Optional[float]:
    """Calculate mean rainfall in mm across all records."""
    if not records:
        return None
    rains = [float(r["rainfall"]) for r in records if "rainfall" in r]
    return round(statistics.mean(rains), 2) if rains else None


def calculate_average_humidity(records: List[Dict[str, Any]]) -> Optional[float]:
    """Calculate mean humidity percentage across records."""
    if not records:
        return None
    hums = [float(r["humidity"]) for r in records if "humidity" in r]
    return round(statistics.mean(hums), 2) if hums else None


def calculate_rainy_days(records: List[Dict[str, Any]], threshold: float = 0.1) -> int:
    """
    Count number of days with rainfall greater than or equal to configured threshold.
    Default threshold is 0.1 mm.
    """
    if not records:
        return 0
    return sum(1 for r in records if float(r.get("rainfall", 0.0)) >= threshold)


def calculate_temperature_trend(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Determine linear trend / slope of temperature over time.
    Returns trend description ('Warming', 'Cooling', or 'Stable') and rate of change.
    """
    if len(records) < 2:
        return {"trend": "Insufficient Data", "slope": 0.0, "description": "Need at least 2 records"}

    temps = [float(r["temperature"]) for r in records]
    n = len(temps)
    x = list(range(n))
    mean_x = statistics.mean(x)
    mean_y = statistics.mean(temps)

    numer = sum((x[i] - mean_x) * (temps[i] - mean_y) for i in range(n))
    denom = sum((x[i] - mean_x) ** 2 for i in range(n))

    slope = numer / denom if denom != 0 else 0.0
    slope = round(slope, 3)

    if slope > 0.15:
        direction = "Warming (Increasing)"
    elif slope < -0.15:
        direction = "Cooling (Decreasing)"
    else:
        direction = "Stable"

    return {
        "trend": direction,
        "slope": slope,
        "first_temp": temps[0],
        "last_temp": temps[-1],
        "net_change": round(temps[-1] - temps[0], 2),
    }


def calculate_rainfall_trend(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Determine rainfall trend over the observation period.
    """
    if len(records) < 2:
        return {"trend": "Insufficient Data", "total": calculate_total_rainfall(records)}

    rains = [float(r["rainfall"]) for r in records]
    half = len(rains) // 2
    first_half_avg = statistics.mean(rains[:half]) if half > 0 else 0.0
    second_half_avg = statistics.mean(rains[half:]) if half > 0 else 0.0

    diff = round(second_half_avg - first_half_avg, 2)
    if diff > 1.0:
        trend_name = "Increasing Precipitation"
    elif diff < -1.0:
        trend_name = "Decreasing Precipitation"
    else:
        trend_name = "Consistent Precipitation"

    return {
        "trend": trend_name,
        "difference": diff,
        "first_half_mean": round(first_half_avg, 2),
        "second_half_mean": round(second_half_avg, 2),
        "total_rainfall": calculate_total_rainfall(records),
    }


def calculate_wind_statistics(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate average, maximum, and minimum wind speed."""
    if not records:
        return {"average": None, "max": None, "min": None}

    winds = [float(r["wind_speed"]) for r in records if "wind_speed" in r]
    if not winds:
        return {"average": None, "max": None, "min": None}

    highest = max(records, key=lambda r: float(r.get("wind_speed", 0.0)))
    return {
        "average": round(statistics.mean(winds), 2),
        "max": {
            "value": round(float(highest["wind_speed"]), 2),
            "date": highest.get("date"),
            "city": highest.get("city"),
        },
        "min": round(min(winds), 2),
    }


def generate_summary(
    records: List[Dict[str, Any]],
    rain_threshold: float = 0.1,
) -> Dict[str, Any]:
    """
    Produce a complete dictionary containing all statistical measurements.
    """
    if not records:
        return {
            "record_count": 0,
            "message": "No weather data records available for analysis.",
        }

    return {
        "record_count": len(records),
        "date_range": {
            "start": records[0].get("date"),
            "end": records[-1].get("date"),
        },
        "temperature": {
            "average": calculate_average_temperature(records),
            "max": calculate_max_temperature(records),
            "min": calculate_min_temperature(records),
            "trend": calculate_temperature_trend(records),
        },
        "rainfall": {
            "total": calculate_total_rainfall(records),
            "average": calculate_average_rainfall(records),
            "rainy_days": calculate_rainy_days(records, threshold=rain_threshold),
            "rainy_day_threshold": rain_threshold,
            "trend": calculate_rainfall_trend(records),
        },
        "humidity": {
            "average": calculate_average_humidity(records),
        },
        "wind_speed": calculate_wind_statistics(records),
    }
