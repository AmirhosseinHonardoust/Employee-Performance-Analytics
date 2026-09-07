from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from src.create_db import REQUIRED_COLUMNS, load_csv_to_db, validate_employees_df


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


def _valid_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "employee_id": ["E1"],
            "name": ["Alice"],
            "department": ["Engineering"],
            "role": ["Dev"],
            "date": ["2024-01-01"],
            "tasks_completed": [8],
            "hours_worked": [7.0],
            "rating": [4.2],
            "projects": [1],
            "absences": [0],
        }
    )


def test_validate_employees_df_accepts_valid_row() -> None:
    validate_employees_df(_valid_df())  # should not raise


def test_validate_employees_df_rejects_nulls() -> None:
    df = _valid_df()
    df.loc[0, "rating"] = None
    with pytest.raises(ValueError, match="null values"):
        validate_employees_df(df)


def test_validate_employees_df_rejects_out_of_range_rating() -> None:
    df = _valid_df()
    df.loc[0, "rating"] = 5.5
    with pytest.raises(ValueError, match="rating"):
        validate_employees_df(df)


def test_validate_employees_df_rejects_bad_absences() -> None:
    df = _valid_df()
    df.loc[0, "absences"] = 2
    with pytest.raises(ValueError, match="absences"):
        validate_employees_df(df)


def test_validate_employees_df_rejects_negative_hours() -> None:
    df = _valid_df()
    df.loc[0, "hours_worked"] = -1.0
    with pytest.raises(ValueError, match="hours_worked"):
        validate_employees_df(df)


def test_load_csv_to_db_rejects_invalid_rating(tmp_path: Path) -> None:
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text(
        "employee_id,name,department,role,date,tasks_completed,hours_worked,"
        "rating,projects,absences\nE1,Alice,Engineering,Dev,2024-01-01,8,7.0,9.9,1,0\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="rating"):
        load_csv_to_db(bad_csv, tmp_path / "hr.db")
