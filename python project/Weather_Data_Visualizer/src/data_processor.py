"""
Data Processing Module
File: src/data_processor.py
Purpose: Clean, normalize, sort, and prepare weather datasets for analytics and visualization.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional


def sort_by_date(records: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Sort weather records chronologically by date.
    Safe against non-standard formats by parsing datetime.
    """
    def _date_key(item: Dict[str, Any]):
        d_val = item.get("date", "")
        try:
            return datetime.strptime(str(d_val).strip(), "%Y-%m-%d")
        except Exception:
            return datetime.min

    return sorted(records, key=_date_key, reverse=reverse)


def normalize_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ensure all fields in records have standard types and whitespace trimmed.
    City is capitalized nicely, numbers are floats, dates are formatted YYYY-MM-DD.
    """
    normalized = []
    for r in records:
        try:
            # Parse and format date consistently
            d_str = str(r["date"]).strip()
            # Try to standardise date format
            try:
                parsed_dt = datetime.strptime(d_str, "%Y-%m-%d")
                clean_date = parsed_dt.strftime("%Y-%m-%d")
            except ValueError:
                clean_date = d_str

            clean_item = {
                "date": clean_date,
                "city": str(r["city"]).strip().title(),
                "temperature": round(float(r["temperature"]), 2),
                "rainfall": round(float(r["rainfall"]), 2),
                "humidity": round(float(r["humidity"]), 1),
                "wind_speed": round(float(r["wind_speed"]), 2),
            }
            normalized.append(clean_item)
        except (ValueError, KeyError, TypeError):
            # Skip invalid item in normalization
            continue
    return normalized


def clean_data(
    records: List[Dict[str, Any]],
    remove_duplicates: bool = True,
    fill_missing: bool = False,
    default_fill: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Clean raw weather dataset:
    - Removes empty or corrupted entries
    - Optionally removes duplicate entries (same date and city)
    - Normalizes data types
    """
    if not records:
        return []

    # Filter out entries missing crucial keys
    clean_list: List[Dict[str, Any]] = []
    seen = set()

    for item in records:
        if not isinstance(item, dict):
            continue

        # Check critical fields
        if not item.get("date") or not item.get("city"):
            continue

        try:
            temp = float(item["temperature"])
            rain = float(item["rainfall"])
            hum = float(item["humidity"])
            wind = float(item["wind_speed"])
        except (KeyError, ValueError, TypeError):
            if fill_missing and default_fill:
                temp = float(item.get("temperature", default_fill.get("temperature", 25.0)))
                rain = float(item.get("rainfall", default_fill.get("rainfall", 0.0)))
                hum = float(item.get("humidity", default_fill.get("humidity", 50.0)))
                wind = float(item.get("wind_speed", default_fill.get("wind_speed", 10.0)))
            else:
                continue

        clean_item = {
            "date": str(item["date"]).strip(),
            "city": str(item["city"]).strip().title(),
            "temperature": round(temp, 2),
            "rainfall": round(rain, 2),
            "humidity": round(hum, 1),
            "wind_speed": round(wind, 2),
        }

        if remove_duplicates:
            key = (clean_item["date"], clean_item["city"].lower())
            if key in seen:
                continue
            seen.add(key)

        clean_list.append(clean_item)

    return sort_by_date(clean_list)


def prepare_analysis_data(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract structured columns for fast vectorized-like analysis and plotting.
    Returns dictionary with parallel lists: dates, cities, temperatures, rainfalls, humidities, wind_speeds.
    """
    sorted_records = sort_by_date(records)
    return {
        "dates": [r["date"] for r in sorted_records],
        "cities": [r["city"] for r in sorted_records],
        "temperatures": [r["temperature"] for r in sorted_records],
        "rainfalls": [r["rainfall"] for r in sorted_records],
        "humidities": [r["humidity"] for r in sorted_records],
        "wind_speeds": [r["wind_speed"] for r in sorted_records],
        "records": sorted_records,
        "count": len(sorted_records),
    }
