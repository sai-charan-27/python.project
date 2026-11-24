"""
Unit tests for Validator Module
File: tests/test_validator.py
"""

import pytest
from src.validator import (
    validate_temperature,
    validate_rainfall,
    validate_humidity,
    validate_wind_speed,
    validate_date,
    validate_city,
    validate_csv_headers,
    validate_record,
)


class TestValidator:

    def test_validate_temperature_valid(self):
        ok, err = validate_temperature(25.5)
        assert ok is True
        assert err is None

        ok, err = validate_temperature("30.1")
        assert ok is True

    def test_validate_temperature_out_of_bounds(self):
        # Exceeds max
        ok, err = validate_temperature(65.0, min_temp=-50.0, max_temp=60.0)
        assert ok is False
        assert "outside valid range" in err

        # Below min
        ok, err = validate_temperature(-60.0, min_temp=-50.0, max_temp=60.0)
        assert ok is False
        assert "outside valid range" in err

    def test_validate_temperature_invalid_type(self):
        ok, err = validate_temperature("abc")
        assert ok is False
        assert "must be numeric" in err

    def test_validate_rainfall_valid(self):
        ok, err = validate_rainfall(0.0)
        assert ok is True

        ok, err = validate_rainfall("12.4")
        assert ok is True

    def test_validate_rainfall_negative(self):
        ok, err = validate_rainfall(-5.0)
        assert ok is False
        assert "cannot be negative" in err

    def test_validate_rainfall_excessive(self):
        ok, err = validate_rainfall(1500.0, max_rain=1000.0)
        assert ok is False
        assert "exceeds configured maximum" in err

    def test_validate_humidity_valid(self):
        ok, err = validate_humidity(55.0)
        assert ok is True

        ok, err = validate_humidity(0.0)
        assert ok is True

        ok, err = validate_humidity(100.0)
        assert ok is True

    def test_validate_humidity_out_of_bounds(self):
        ok, err = validate_humidity(-1.0)
        assert ok is False

        ok, err = validate_humidity(105.0)
        assert ok is False

    def test_validate_wind_speed_valid(self):
        ok, err = validate_wind_speed(15.2)
        assert ok is True

    def test_validate_wind_speed_negative(self):
        ok, err = validate_wind_speed(-2.0)
        assert ok is False

    def test_validate_wind_speed_configurable_limit(self):
        ok, err = validate_wind_speed(90.0, max_wind=80.0)
        assert ok is False
        assert "exceeds maximum configured limit" in err

    def test_validate_date_valid(self):
        ok, err = validate_date("2026-11-24")
        assert ok is True
        assert err is None

    def test_validate_date_invalid_format(self):
        ok, err = validate_date("24/11/2026")
        assert ok is False
        assert "does not match expected format" in err

        ok, err = validate_date("not-a-date")
        assert ok is False

    def test_validate_date_empty(self):
        ok, err = validate_date("")
        assert ok is False

    def test_validate_city(self):
        ok, err = validate_city("Hyderabad")
        assert ok is True

        ok, err = validate_city("")
        assert ok is False

        ok, err = validate_city("   ")
        assert ok is False

    def test_validate_csv_headers(self):
        required = ["date", "city", "temperature", "rainfall", "humidity", "wind_speed"]
        ok, missing = validate_csv_headers(required)
        assert ok is True
        assert len(missing) == 0

        # Missing humidity
        bad_headers = ["date", "city", "temperature", "rainfall", "wind_speed"]
        ok, missing = validate_csv_headers(bad_headers)
        assert ok is False
        assert any("humidity" in m for m in missing)

    def test_validate_record_complete_valid(self):
        record = {
            "date": "2026-11-01",
            "city": "Hyderabad",
            "temperature": 29.5,
            "rainfall": 0.0,
            "humidity": 48,
            "wind_speed": 12.5,
        }
        ok, errors = validate_record(record)
        assert ok is True
        assert len(errors) == 0

    def test_validate_record_multiple_errors(self):
        bad_record = {
            "date": "bad-date",
            "city": "",
            "temperature": 999.0,
            "rainfall": -10.0,
            "humidity": 150.0,
            "wind_speed": -5.0,
        }
        ok, errors = validate_record(bad_record)
        assert ok is False
        assert len(errors) >= 5
