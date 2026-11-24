"""
Search and Filter Module
File: src/search.py
Purpose: Search and filter weather records by city, date, temperature, rainfall, humidity, and keywords.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional


def search_by_city(
    records: List[Dict[str, Any]],
    city_name: str,
    exact_match: bool = False,
) -> List[Dict[str, Any]]:
    """
    Search records matching city name (case-insensitive).
    """
    if not city_name or not city_name.strip():
        return records

    query = city_name.strip().lower()
    results = []
    for r in records:
        city = str(r.get("city", "")).lower()
        if exact_match and city == query:
            results.append(r)
        elif not exact_match and query in city:
            results.append(r)
    return results


def search_by_date(
    records: List[Dict[str, Any]],
    target_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Search records for an exact date or within an inclusive date range [start_date, end_date].
    Dates should be in 'YYYY-MM-DD' format.
    """
    results = []

    def _parse(d_str: Optional[str]):
        if not d_str:
            return None
        try:
            return datetime.strptime(d_str.strip(), "%Y-%m-%d")
        except ValueError:
            return None

    dt_target = _parse(target_date)
    dt_start = _parse(start_date)
    dt_end = _parse(end_date)

    for r in records:
        r_dt = _parse(r.get("date"))
        if not r_dt:
            continue

        if dt_target is not None:
            if r_dt == dt_target:
                results.append(r)
            continue

        matches_start = True if dt_start is None else (r_dt >= dt_start)
        matches_end = True if dt_end is None else (r_dt <= dt_end)

        if matches_start and matches_end:
            results.append(r)

    return results


def filter_by_temperature(
    records: List[Dict[str, Any]],
    min_temp: Optional[float] = None,
    max_temp: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """Filter records within an inclusive temperature range [min_temp, max_temp]."""
    results = []
    for r in records:
        try:
            temp = float(r.get("temperature", 0.0))
            if min_temp is not None and temp < min_temp:
                continue
            if max_temp is not None and temp > max_temp:
                continue
            results.append(r)
        except (ValueError, TypeError):
            continue
    return results


def filter_by_rainfall(
    records: List[Dict[str, Any]],
    min_rain: Optional[float] = None,
    max_rain: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """Filter records within an inclusive rainfall range [min_rain, max_rain]."""
    results = []
    for r in records:
        try:
            rain = float(r.get("rainfall", 0.0))
            if min_rain is not None and rain < min_rain:
                continue
            if max_rain is not None and rain > max_rain:
                continue
            results.append(r)
        except (ValueError, TypeError):
            continue
    return results


def filter_by_humidity(
    records: List[Dict[str, Any]],
    min_hum: Optional[float] = None,
    max_hum: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """Filter records within an inclusive humidity range [min_hum, max_hum]."""
    results = []
    for r in records:
        try:
            hum = float(r.get("humidity", 0.0))
            if min_hum is not None and hum < min_hum:
                continue
            if max_hum is not None and hum > max_hum:
                continue
            results.append(r)
        except (ValueError, TypeError):
            continue
    return results


def search_by_keyword(records: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
    """
    Search across all string representations of the record fields for a keyword.
    """
    if not keyword or not keyword.strip():
        return records

    kw = keyword.strip().lower()
    results = []
    for r in records:
        combined_text = " ".join(str(v).lower() for v in r.values())
        if kw in combined_text:
            results.append(r)
    return results


def filter_records(records: List[Dict[str, Any]], **criteria) -> List[Dict[str, Any]]:
    """
    Composite filter applying multiple criteria simultaneously:
    - city: str
    - date: str
    - start_date, end_date: str
    - min_temp, max_temp: float
    - min_rain, max_rain: float
    - min_hum, max_hum: float
    - keyword: str
    """
    filtered = list(records)

    if criteria.get("city"):
        filtered = search_by_city(filtered, criteria["city"])

    if criteria.get("date") or criteria.get("start_date") or criteria.get("end_date"):
        filtered = search_by_date(
            filtered,
            target_date=criteria.get("date"),
            start_date=criteria.get("start_date"),
            end_date=criteria.get("end_date"),
        )

    if criteria.get("min_temp") is not None or criteria.get("max_temp") is not None:
        filtered = filter_by_temperature(
            filtered,
            min_temp=criteria.get("min_temp"),
            max_temp=criteria.get("max_temp"),
        )

    if criteria.get("min_rain") is not None or criteria.get("max_rain") is not None:
        filtered = filter_by_rainfall(
            filtered,
            min_rain=criteria.get("min_rain"),
            max_rain=criteria.get("max_rain"),
        )

    if criteria.get("min_hum") is not None or criteria.get("max_hum") is not None:
        filtered = filter_by_humidity(
            filtered,
            min_hum=criteria.get("min_hum"),
            max_hum=criteria.get("max_hum"),
        )

    if criteria.get("keyword"):
        filtered = search_by_keyword(filtered, criteria["keyword"])

    return filtered
