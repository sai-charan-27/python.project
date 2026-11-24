"""
Validation Module
File: src/validator.py
Purpose: Ensure that weather records contain valid information and meet configurable ranges.
"""

from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

# Default configuration for validation limits
# These ranges are configurable per dataset or user preferences
DEFAULT_CONFIG = {
    "min_temperature": -50.0,
    "max_temperature": 60.0,
    "min_rainfall": 0.0,
    "max_rainfall": 1000.0,
    "min_humidity": 0.0,
    "max_humidity": 100.0,
    "min_wind_speed": 0.0,
    "max_wind_speed": 250.0,
    "date_format": "%Y-%m-%d",
    "required_columns": ["date", "city", "temperature", "rainfall", "humidity", "wind_speed"],
}


def validate_temperature(
    temp: Any,
    min_temp: Optional[float] = None,
    max_temp: Optional[float] = None,
) -> Tuple[bool, Optional[str]]:
    """Validate temperature value against numeric type and configured limits."""
    if min_temp is None:
        min_temp = DEFAULT_CONFIG["min_temperature"]
    if max_temp is None:
        max_temp = DEFAULT_CONFIG["max_temperature"]

    try:
        val = float(temp)
    except (ValueError, TypeError):
        return False, f"Temperature must be numeric, got: {temp!r}"

    if val < min_temp or val > max_temp:
        return False, f"Temperature {val}°C is outside valid range [{min_temp}, {max_temp}]°C"

    return True, None


def validate_rainfall(
    rainfall: Any,
    min_rain: Optional[float] = None,
    max_rain: Optional[float] = None,
) -> Tuple[bool, Optional[str]]:
    """Validate rainfall value against numeric non-negative type and configured limit."""
    if min_rain is None:
        min_rain = DEFAULT_CONFIG["min_rainfall"]
    if max_rain is None:
        max_rain = DEFAULT_CONFIG["max_rainfall"]

    try:
        val = float(rainfall)
    except (ValueError, TypeError):
        return False, f"Rainfall must be numeric, got: {rainfall!r}"

    if val < min_rain:
        return False, f"Rainfall cannot be negative ({val} mm < {min_rain} mm)"
    if val > max_rain:
        return False, f"Rainfall {val} mm exceeds configured maximum {max_rain} mm"

    return True, None


def validate_humidity(
    humidity: Any,
    min_hum: Optional[float] = None,
    max_hum: Optional[float] = None,
) -> Tuple[bool, Optional[str]]:
    """Validate relative humidity percentage (0 - 100%)."""
    if min_hum is None:
        min_hum = DEFAULT_CONFIG["min_humidity"]
    if max_hum is None:
        max_hum = DEFAULT_CONFIG["max_humidity"]

    try:
        val = float(humidity)
    except (ValueError, TypeError):
        return False, f"Humidity must be numeric, got: {humidity!r}"

    if val < min_hum or val > max_hum:
        return False, f"Humidity {val}% must be between {min_hum}% and {max_hum}%"

    return True, None


def validate_wind_speed(
    wind_speed: Any,
    min_wind: Optional[float] = None,
    max_wind: Optional[float] = None,
) -> Tuple[bool, Optional[str]]:
    """Validate wind speed (numeric, non-negative, within configured bounds)."""
    if min_wind is None:
        min_wind = DEFAULT_CONFIG["min_wind_speed"]
    if max_wind is None:
        max_wind = DEFAULT_CONFIG["max_wind_speed"]

    try:
        val = float(wind_speed)
    except (ValueError, TypeError):
        return False, f"Wind speed must be numeric, got: {wind_speed!r}"

    if val < min_wind:
        return False, f"Wind speed cannot be negative ({val} km/h < {min_wind} km/h)"
    if val > max_wind:
        return False, f"Wind speed {val} km/h exceeds maximum configured limit {max_wind} km/h"

    return True, None


def validate_date(date_val: Any, date_format: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Validate that the date string matches the expected format (YYYY-MM-DD by default)."""
    if date_format is None:
        date_format = DEFAULT_CONFIG["date_format"]

    if not isinstance(date_val, str) or not date_val.strip():
        return False, f"Date cannot be empty, got: {date_val!r}"

    try:
        parsed_date = datetime.strptime(date_val.strip(), date_format)
        # Year sanity check (1800 to 2200)
        if parsed_date.year < 1800 or parsed_date.year > 2200:
            return False, f"Year {parsed_date.year} is out of realistic calendar bounds (1800-2200)"
        return True, None
    except ValueError:
        return False, f"Date {date_val!r} does not match expected format {date_format}"


def validate_city(city_val: Any) -> Tuple[bool, Optional[str]]:
    """Validate city name (non-empty string)."""
    if not isinstance(city_val, str) or not city_val.strip():
        return False, "City name cannot be empty"
    return True, None


def validate_csv_headers(
    headers: List[str],
    required_columns: Optional[List[str]] = None,
) -> Tuple[bool, List[str]]:
    """Check that required columns exist in CSV header list."""
    if required_columns is None:
        required_columns = DEFAULT_CONFIG["required_columns"]

    normalized_headers = [h.strip().lower() for h in headers if isinstance(h, str)]
    missing = [col for col in required_columns if col.lower() not in normalized_headers]

    if missing:
        return False, [f"Missing required CSV column: '{col}'" for col in missing]
    return True, []


def validate_record(
    record: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """
    Validate a complete weather record dictionary.
    Returns (is_valid, list_of_error_strings).
    """
    cfg = DEFAULT_CONFIG.copy()
    if config:
        cfg.update(config)

    errors: List[str] = []

    # 1. Date check
    if "date" not in record:
        errors.append("Field 'date' is missing")
    else:
        ok, err = validate_date(record["date"], cfg.get("date_format"))
        if not ok and err:
            errors.append(err)

    # 2. City check
    if "city" not in record:
        errors.append("Field 'city' is missing")
    else:
        ok, err = validate_city(record["city"])
        if not ok and err:
            errors.append(err)

    # 3. Temperature check
    if "temperature" not in record:
        errors.append("Field 'temperature' is missing")
    else:
        ok, err = validate_temperature(
            record["temperature"],
            cfg.get("min_temperature"),
            cfg.get("max_temperature"),
        )
        if not ok and err:
            errors.append(err)

    # 4. Rainfall check
    if "rainfall" not in record:
        errors.append("Field 'rainfall' is missing")
    else:
        ok, err = validate_rainfall(
            record["rainfall"],
            cfg.get("min_rainfall"),
            cfg.get("max_rainfall"),
        )
        if not ok and err:
            errors.append(err)

    # 5. Humidity check
    if "humidity" not in record:
        errors.append("Field 'humidity' is missing")
    else:
        ok, err = validate_humidity(
            record["humidity"],
            cfg.get("min_humidity"),
            cfg.get("max_humidity"),
        )
        if not ok and err:
            errors.append(err)

    # 6. Wind speed check
    if "wind_speed" not in record:
        errors.append("Field 'wind_speed' is missing")
    else:
        ok, err = validate_wind_speed(
            record["wind_speed"],
            cfg.get("min_wind_speed"),
            cfg.get("max_wind_speed"),
        )
        if not ok and err:
            errors.append(err)

    return (len(errors) == 0), errors
