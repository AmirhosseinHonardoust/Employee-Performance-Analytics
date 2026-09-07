from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from src.create_db import REQUIRED_COLUMNS, load_csv_to_db


def test_load_csv_to_db_creates_table(tmp_path: Path, sample_csv: Path) -> None:
    db_path = tmp_path / "hr.db"

    load_csv_to_db(sample_csv, db_path)

    assert db_path.exists()
    with sqlite3.connect(db_path) as con:
        df = pd.read_sql_query("SELECT * FROM employees ORDER BY employee_id, date;", con)

    assert len(df) == 5
    assert list(df.columns) == REQUIRED_COLUMNS
    assert df["date"].iloc[0] == "2024-01-01"


def test_load_csv_to_db_missing_csv_raises(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.csv"
    db_path = tmp_path / "hr.db"

    with pytest.raises(FileNotFoundError):
        load_csv_to_db(missing, db_path)


def test_load_csv_to_db_missing_columns_raises(tmp_path: Path) -> None:
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("employee_id,name\nE1,Alice\n", encoding="utf-8")
    db_path = tmp_path / "hr.db"

    with pytest.raises(ValueError, match="missing required columns"):
        load_csv_to_db(bad_csv, db_path)


def test_load_csv_to_db_replaces_existing_table(tmp_path: Path, sample_csv: Path) -> None:
    db_path = tmp_path / "hr.db"

    load_csv_to_db(sample_csv, db_path)
    load_csv_to_db(sample_csv, db_path)  # should not fail or duplicate rows

    with sqlite3.connect(db_path) as con:
        (count,) = con.execute("SELECT COUNT(*) FROM employees;").fetchone()

    assert count == 5
