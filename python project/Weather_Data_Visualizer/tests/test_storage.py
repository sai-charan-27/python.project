"""
Unit tests for Storage Module
File: tests/test_storage.py
"""

import pytest
from pathlib import Path
from src.storage import (
    save_to_csv,
    load_from_csv,
    save_to_json,
    load_from_json,
    backup_data,
    restore_data,
)


@pytest.fixture
def dummy_records():
    return [
        {"date": "2026-11-01", "city": "Hyderabad", "temperature": 29.5, "rainfall": 0.0, "humidity": 48.0, "wind_speed": 12.5},
        {"date": "2026-11-02", "city": "Hyderabad", "temperature": 30.1, "rainfall": 2.4, "humidity": 55.0, "wind_speed": 14.2},
    ]


class TestStorage:

    def test_csv_save_and_load(self, tmp_path, dummy_records):
        csv_path = tmp_path / "test_data.csv"
        ok_save, msg_save = save_to_csv(dummy_records, str(csv_path))
        assert ok_save is True
        assert csv_path.exists()

        loaded, msg_load = load_from_csv(str(csv_path))
        assert len(loaded) == len(dummy_records)
        assert loaded[0]["city"] == "Hyderabad"
        assert loaded[1]["temperature"] == 30.1

    def test_json_save_and_load(self, tmp_path, dummy_records):
        json_path = tmp_path / "test_data.json"
        ok_save, msg_save = save_to_json(dummy_records, str(json_path))
        assert ok_save is True
        assert json_path.exists()

        loaded, msg_load = load_from_json(str(json_path))
        assert len(loaded) == len(dummy_records)
        assert loaded[0]["city"] == "Hyderabad"
        assert loaded[0]["temperature"] == 29.5

    def test_load_non_existent_files(self):
        records, msg = load_from_csv("does_not_exist_file.csv")
        assert records == []
        assert "does not exist" in msg.lower()

        records, msg = load_from_json("does_not_exist_file.json")
        assert records == []
        assert "does not exist" in msg.lower()

    def test_corrupted_json_handling(self, tmp_path):
        bad_json = tmp_path / "corrupted.json"
        bad_json.write_text("{ this is invalid json !!!", encoding="utf-8")

        records, msg = load_from_json(str(bad_json))
        assert records == []
        assert "corrupted" in msg.lower()

    def test_backup_and_restore(self, tmp_path, dummy_records):
        source = tmp_path / "source.csv"
        save_to_csv(dummy_records, str(source))

        backup_dir = tmp_path / "backups"
        ok_b, backup_file = backup_data(str(source), str(backup_dir))
        assert ok_b is True
        assert Path(backup_file).exists()

        # Overwrite source with empty/different file
        source.write_text("empty\n", encoding="utf-8")

        # Restore from backup
        ok_r, msg_r = restore_data(backup_file, str(source))
        assert ok_r is True

        restored_records, _ = load_from_csv(str(source))
        assert len(restored_records) == 2
