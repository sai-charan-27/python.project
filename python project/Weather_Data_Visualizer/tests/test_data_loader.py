"""
Unit tests for Data Loader Module
File: tests/test_data_loader.py
"""

import pytest
from pathlib import Path
from src.data_loader import (
    check_csv_structure,
    parse_weather_data,
    load_csv_file,
    load_sample_data,
)


class TestDataLoader:

    def test_check_csv_structure_valid(self, tmp_path):
        csv_file = tmp_path / "valid.csv"
        csv_file.write_text("date,city,temperature,rainfall,humidity,wind_speed\n2026-11-01,Hyderabad,29.5,0.0,48,12.5\n", encoding="utf-8")

        ok, headers, issues = check_csv_structure(str(csv_file))
        assert ok is True
        assert len(headers) == 6
        assert len(issues) == 0

    def test_check_csv_structure_missing_file(self):
        ok, headers, issues = check_csv_structure("non_existent_file_xyz.csv")
        assert ok is False
        assert any("does not exist" in i for i in issues)

    def test_check_csv_structure_missing_columns(self, tmp_path):
        csv_file = tmp_path / "missing_cols.csv"
        csv_file.write_text("date,city,temp\n", encoding="utf-8")

        ok, headers, issues = check_csv_structure(str(csv_file))
        assert ok is False
        assert len(issues) > 0

    def test_parse_weather_data(self):
        raw_rows = [
            {"date": "2026-11-01", "city": "Hyderabad", "temperature": "29.5", "rainfall": "0.0", "humidity": "48", "wind_speed": "12.5"},
            {"date": "2026-11-02", "city": "Hyderabad", "temperature": "30.1", "rainfall": "2.4", "humidity": "55", "wind_speed": "14.2"},
            {"date": "invalid-date", "city": "Hyderabad", "temperature": "30.1", "rainfall": "2.4", "humidity": "55", "wind_speed": "14.2"},
        ]

        valid, invalid = parse_weather_data(raw_rows)
        assert len(valid) == 2
        assert len(invalid) == 1
        assert valid[0]["city"] == "Hyderabad"
        assert isinstance(valid[0]["temperature"], float)

    def test_load_sample_data(self):
        valid, invalid, errors = load_sample_data()
        assert len(errors) == 0
        assert len(valid) >= 7
        assert valid[0]["date"] == "2026-11-01"
