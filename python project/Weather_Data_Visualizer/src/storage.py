"""
Storage Module
File: src/storage.py
Purpose: Save, load, update, backup, and restore weather data records in CSV and JSON formats.
Ensures application resilience against missing or corrupted files.
"""

import csv
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple

from src.validator import validate_record

logger = logging.getLogger(__name__)

FIELDNAMES = ["date", "city", "temperature", "rainfall", "humidity", "wind_speed"]


def save_to_csv(records: List[Dict[str, Any]], file_path: str) -> Tuple[bool, str]:
    """
    Save list of weather records to CSV file.
    Creates parent directories if missing.
    Returns: (success: bool, message: str)
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for r in records:
                # Format each field appropriately
                row = {
                    "date": r.get("date", ""),
                    "city": r.get("city", ""),
                    "temperature": r.get("temperature", ""),
                    "rainfall": r.get("rainfall", ""),
                    "humidity": r.get("humidity", ""),
                    "wind_speed": r.get("wind_speed", ""),
                }
                writer.writerow(row)
        return True, f"Successfully saved {len(records)} records to CSV: {file_path}"
    except Exception as e:
        logger.error(f"Error saving to CSV {file_path}: {e}")
        return False, f"Failed to save CSV file: {str(e)}"


def load_from_csv(file_path: str) -> Tuple[List[Dict[str, Any]], str]:
    """
    Load weather records from CSV file.
    Gracefully handles missing and corrupted files.
    Returns: (records: list, message: str)
    """
    path = Path(file_path)
    if not path.exists():
        return [], f"File does not exist: {file_path}"

    records: List[Dict[str, Any]] = []
    try:
        with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=1):
                try:
                    rec = {
                        "date": str(row["date"]).strip(),
                        "city": str(row["city"]).strip(),
                        "temperature": float(row["temperature"]),
                        "rainfall": float(row["rainfall"]),
                        "humidity": float(row["humidity"]),
                        "wind_speed": float(row["wind_speed"]),
                    }
                    records.append(rec)
                except Exception as row_err:
                    logger.warning(f"Skipping corrupted row {idx} in {file_path}: {row_err}")
                    continue
        return records, f"Loaded {len(records)} records from CSV"
    except Exception as e:
        logger.error(f"Failed to read CSV {file_path}: {e}")
        return [], f"Corrupted or unreadable CSV file: {str(e)}"


def save_to_json(records: List[Dict[str, Any]], file_path: str, indent: int = 2) -> Tuple[bool, str]:
    """
    Save list of weather records to JSON file.
    Creates parent directories if missing.
    Returns: (success: bool, message: str)
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, mode="w", encoding="utf-8") as f:
            json.dump(records, f, indent=indent, ensure_ascii=False)
        return True, f"Successfully saved {len(records)} records to JSON: {file_path}"
    except Exception as e:
        logger.error(f"Error saving to JSON {file_path}: {e}")
        return False, f"Failed to save JSON file: {str(e)}"


def load_from_json(file_path: str) -> Tuple[List[Dict[str, Any]], str]:
    """
    Load weather records from JSON file.
    Gracefully handles missing and corrupted files.
    Returns: (records: list, message: str)
    """
    path = Path(file_path)
    if not path.exists():
        return [], f"File does not exist: {file_path}"

    try:
        with open(path, mode="r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return [], f"Invalid JSON format: expected list of records, got {type(data).__name__}"

        valid_records = []
        for idx, item in enumerate(data):
            if isinstance(item, dict):
                try:
                    rec = {
                        "date": str(item["date"]).strip(),
                        "city": str(item["city"]).strip(),
                        "temperature": float(item["temperature"]),
                        "rainfall": float(item["rainfall"]),
                        "humidity": float(item["humidity"]),
                        "wind_speed": float(item["wind_speed"]),
                    }
                    valid_records.append(rec)
                except Exception as e:
                    logger.warning(f"Skipping invalid item #{idx} in JSON: {e}")
        return valid_records, f"Loaded {len(valid_records)} records from JSON"
    except json.JSONDecodeError as err:
        logger.error(f"Corrupted JSON in {file_path}: {err}")
        return [], f"Corrupted JSON file ({str(err)})"
    except Exception as e:
        logger.error(f"Error loading JSON {file_path}: {e}")
        return [], f"Failed to load JSON: {str(e)}"


def backup_data(source_path: str, backup_dir: str = "data/backups") -> Tuple[bool, str]:
    """
    Create a timestamped backup copy of a given data file.
    Returns: (success: bool, backup_file_path_or_error: str)
    """
    src = Path(source_path)
    if not src.exists():
        return False, f"Source file does not exist for backup: {source_path}"

    try:
        b_dir = Path(backup_dir)
        b_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{src.stem}_backup_{timestamp}{src.suffix}"
        backup_dest = b_dir / backup_filename

        shutil.copy2(src, backup_dest)
        return True, str(backup_dest)
    except Exception as e:
        logger.error(f"Failed to create backup for {source_path}: {e}")
        return False, f"Backup failed: {str(e)}"


def restore_data(backup_file: str, target_path: str) -> Tuple[bool, str]:
    """
    Restore data from a backup file to the target path.
    Returns: (success: bool, message: str)
    """
    bk = Path(backup_file)
    if not bk.exists():
        return False, f"Backup file does not exist: {backup_file}"

    try:
        tgt = Path(target_path)
        tgt.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(bk, tgt)
        return True, f"Successfully restored data from {backup_file} to {target_path}"
    except Exception as e:
        logger.error(f"Failed to restore backup {backup_file}: {e}")
        return False, f"Restore failed: {str(e)}"
