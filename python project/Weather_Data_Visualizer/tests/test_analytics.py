"""
Unit tests for Analytics Module
File: tests/test_analytics.py
"""

import pytest
from src.analytics import (
    calculate_average_temperature,
    calculate_max_temperature,
    calculate_min_temperature,
    calculate_total_rainfall,
    calculate_average_rainfall,
    calculate_average_humidity,
    calculate_rainy_days,
    calculate_temperature_trend,
    calculate_rainfall_trend,
    generate_summary,
)


@pytest.fixture
def sample_records():
    return [
        {"date": "2026-11-01", "city": "Hyderabad", "temperature": 29.5, "rainfall": 0.0, "humidity": 48.0, "wind_speed": 12.5},
        {"date": "2026-11-02", "city": "Hyderabad", "temperature": 30.1, "rainfall": 2.4, "humidity": 55.0, "wind_speed": 14.2},
        {"date": "2026-11-03", "city": "Hyderabad", "temperature": 28.7, "rainfall": 5.2, "humidity": 61.0, "wind_speed": 11.8},
        {"date": "2026-11-04", "city": "Hyderabad", "temperature": 27.9, "rainfall": 0.0, "humidity": 52.0, "wind_speed": 10.4},
        {"date": "2026-11-05", "city": "Hyderabad", "temperature": 31.2, "rainfall": 0.0, "humidity": 43.0, "wind_speed": 15.1},
        {"date": "2026-11-06", "city": "Hyderabad", "temperature": 26.8, "rainfall": 8.6, "humidity": 67.0, "wind_speed": 9.7},
        {"date": "2026-11-07", "city": "Hyderabad", "temperature": 29.0, "rainfall": 1.3, "humidity": 58.0, "wind_speed": 13.0},
    ]


class TestAnalytics:

    def test_calculate_average_temperature(self, sample_records):
        avg = calculate_average_temperature(sample_records)
        expected = round((29.5 + 30.1 + 28.7 + 27.9 + 31.2 + 26.8 + 29.0) / 7, 2)
        assert avg == expected

    def test_calculate_max_temperature(self, sample_records):
        result = calculate_max_temperature(sample_records)
        assert result["value"] == 31.2
        assert result["date"] == "2026-11-05"
        assert result["city"] == "Hyderabad"

    def test_calculate_min_temperature(self, sample_records):
        result = calculate_min_temperature(sample_records)
        assert result["value"] == 26.8
        assert result["date"] == "2026-11-06"
        assert result["city"] == "Hyderabad"

    def test_calculate_rainfall_metrics(self, sample_records):
        total = calculate_total_rainfall(sample_records)
        assert total == 17.5

        avg = calculate_average_rainfall(sample_records)
        assert avg == round(17.5 / 7, 2)

    def test_calculate_rainy_days(self, sample_records):
        # Days with rain: Nov 2 (2.4), Nov 3 (5.2), Nov 6 (8.6), Nov 7 (1.3) = 4 days
        count = calculate_rainy_days(sample_records, threshold=0.1)
        assert count == 4

        # Threshold >= 5.0 mm: Nov 3 (5.2), Nov 6 (8.6) = 2 days
        count_high = calculate_rainy_days(sample_records, threshold=5.0)
        assert count_high == 2

    def test_calculate_average_humidity(self, sample_records):
        avg_hum = calculate_average_humidity(sample_records)
        expected = round((48 + 55 + 61 + 52 + 43 + 67 + 58) / 7, 2)
        assert avg_hum == expected

    def test_empty_records_handling(self):
        assert calculate_average_temperature([]) is None
        assert calculate_max_temperature([]) is None
        assert calculate_min_temperature([]) is None
        assert calculate_total_rainfall([]) == 0.0
        assert calculate_rainy_days([]) == 0

    def test_generate_summary_structure(self, sample_records):
        summary = generate_summary(sample_records)
        assert summary["record_count"] == 7
        assert "temperature" in summary
        assert "rainfall" in summary
        assert "humidity" in summary
        assert "wind_speed" in summary
