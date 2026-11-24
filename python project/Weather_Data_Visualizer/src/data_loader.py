"""
Data Loader Module
File: src/data_loader.py
Purpose: Import weather datasets from CSV files, validate columns, and detect malformed records.
"""

import csv
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

from src.validator import validate_csv_headers, validate_record, DEFAULT_CONFIG

logger = logging.getLogger(__name__)


def check_csv_structure(
    file_path: str,
    required_columns: Optional[List[str]] = None,
) -> Tuple[bool, List[str], List[str]]:
    """
    Check if a CSV file exists and has the required column headers.
    Returns: (is_valid, header_columns, list_of_issues)
    """
    path = Path(file_path)
    if not path.exists():
        return False, [], [f"File does not exist: {file_path}"]
    if not path.is_file():
        return False, [], [f"Path is not a regular file: {file_path}"]

    try:
        with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            header_row = next(reader, None)
            if header_row is None:
                return False, [], ["CSV file is completely empty"]
            
            clean_headers = [h.strip() for h in header_row if h is not None]
            ok, errors = validate_csv_headers(clean_headers, required_columns)
            return ok, clean_headers, errors
    except Exception as e:
        logger.error(f"Error checking CSV structure for {file_path}: {e}")
        return False, [], [f"Failed to read CSV structure: {str(e)}"]


def parse_weather_data(
    rows: List[Dict[str, Any]],
    config: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Parse and validate raw row dictionaries from CSV/JSON.
    Returns: (valid_records, invalid_rows_info)
    """
    valid_records: List[Dict[str, Any]] = []
    invalid_rows_info: List[Dict[str, Any]] = []

    for index, raw_row in enumerate(rows, start=1):
        # Normalize keys (strip whitespace and lowercase)
        normalized_row = {
            k.strip().lower(): v.strip() if isinstance(v, str) else v
            for k, v in raw_row.items()
            if k is not None
        }

        # Check required fields exist before type conversion
        is_valid, errors = validate_record(normalized_row, config)
        if not is_valid:
            invalid_rows_info.append({
                "row_index": index,
                "raw_data": raw_row,
                "errors": errors,
            })
            continue

        try:
            # Cast to proper types
            record = {
                "date": str(normalized_row["date"]).strip(),
                "city": str(normalized_row["city"]).strip(),
                "temperature": float(normalized_row["temperature"]),
                "rainfall": float(normalized_row["rainfall"]),
                "humidity": float(normalized_row["humidity"]),
                "wind_speed": float(normalized_row["wind_speed"]),
            }
            valid_records.append(record)
        except Exception as e:
            invalid_rows_info.append({
                "row_index": index,
                "raw_data": raw_row,
                "errors": [f"Type casting error: {str(e)}"],
            })

    return valid_records, invalid_rows_info


def load_csv_file(
    file_path: str,
    config: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
    """
    Load weather data from any CSV file.
    Returns: (valid_records, invalid_rows_info, fatal_errors)
    """
    is_valid_structure, headers, structural_errors = check_csv_structure(file_path)
    if not is_valid_structure:
        return [], [], structural_errors

    path = Path(file_path)
    raw_rows = []
    try:
        with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_rows.append(row)
    except Exception as e:
        return [], [], [f"Failed to read CSV content: {str(e)}"]

    valid_records, invalid_rows = parse_weather_data(raw_rows, config)
    return valid_records, invalid_rows, []


def load_sample_data(
    sample_path: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
    """
    Convenience method to load sample dataset from standard data directory.
    """
    if sample_path is None:
        # Check standard locations
        candidates = [
            Path("data/sample_weather.csv"),
            Path(__file__).resolve().parent.parent / "data" / "sample_weather.csv",
            Path("Weather_Data_Visualizer/data/sample_weather.csv"),
        ]
        found = False
        for cand in candidates:
            if cand.exists():
                sample_path = str(cand)
                found = True
                break
        if not found:
            return [], [], ["Default sample_weather.csv file could not be found."]

    return load_csv_file(sample_path, config)
