"""
Unit tests for Data Processor, Search, Alerts, and Exporter Modules
File: tests/test_additional_modules.py
"""

import pytest
from src.data_processor import clean_data, sort_by_date, prepare_analysis_data
from src.search import search_by_city, search_by_date, filter_by_temperature, filter_by_rainfall, search_by_keyword, filter_records
from src.alerts import check_temperature_threshold, check_rainfall_threshold, check_humidity_threshold, generate_alerts
from src.exporter import export_csv_report, export_text_report, export_markdown_report, generate_report
from src.analytics import generate_summary


@pytest.fixture
def sample_records():
    return [
        {"date": "2026-11-03", "city": "Hyderabad", "temperature": 28.7, "rainfall": 5.2, "humidity": 61.0, "wind_speed": 11.8},
        {"date": "2026-11-01", "city": "Hyderabad", "temperature": 29.5, "rainfall": 0.0, "humidity": 48.0, "wind_speed": 12.5},
        {"date": "2026-11-02", "city": "Bengaluru", "temperature": 24.0, "rainfall": 15.0, "humidity": 85.0, "wind_speed": 14.2},
    ]


def test_sort_by_date(sample_records):
    sorted_recs = sort_by_date(sample_records)
    assert sorted_recs[0]["date"] == "2026-11-01"
    assert sorted_recs[1]["date"] == "2026-11-02"
    assert sorted_recs[2]["date"] == "2026-11-03"


def test_clean_data(sample_records):
    # Duplicate record
    records_with_dup = sample_records + [sample_records[1]]
    cleaned = clean_data(records_with_dup, remove_duplicates=True)
    assert len(cleaned) == 3


def test_prepare_analysis_data(sample_records):
    data = prepare_analysis_data(sample_records)
    assert len(data["dates"]) == 3
    assert len(data["temperatures"]) == 3
    assert data["dates"][0] == "2026-11-01"


def test_search_by_city(sample_records):
    hyd = search_by_city(sample_records, "hyderabad")
    assert len(hyd) == 2
    blr = search_by_city(sample_records, "Bengaluru")
    assert len(blr) == 1


def test_search_by_date(sample_records):
    matched = search_by_date(sample_records, target_date="2026-11-01")
    assert len(matched) == 1
    assert matched[0]["city"] == "Hyderabad"

    range_matched = search_by_date(sample_records, start_date="2026-11-01", end_date="2026-11-02")
    assert len(range_matched) == 2


def test_alerts_detection(sample_records):
    alerts = generate_alerts(sample_records, thresholds={"heavy_rainfall": 10.0, "high_humidity": 80.0})
    assert len(alerts) >= 2  # heavy rain (15mm) and high humidity (85%) in Bengaluru


def test_exporter_generation(tmp_path, sample_records):
    summary = generate_summary(sample_records)
    csv_file = tmp_path / "test_report.csv"
    txt_file = tmp_path / "test_report.txt"
    md_file = tmp_path / "test_report.md"

    export_csv_report(sample_records, summary, str(csv_file))
    export_text_report(sample_records, summary, str(txt_file))
    export_markdown_report(sample_records, summary, str(md_file))

    assert csv_file.exists()
    assert txt_file.exists()
    assert md_file.exists()
    assert "Weather Data Analysis Report" in md_file.read_text(encoding="utf-8")
