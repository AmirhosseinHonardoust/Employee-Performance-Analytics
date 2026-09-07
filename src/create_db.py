#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS employees (
    employee_id     TEXT,
    name            TEXT,
    department      TEXT,
    role            TEXT,
    date            TEXT,
    tasks_completed INTEGER,
    hours_worked    REAL,
    rating          REAL,
    projects        INTEGER,
    absences        INTEGER
);
"""

REQUIRED_COLUMNS = [
    "employee_id",
    "name",
    "department",
    "role",
    "date",
    "tasks_completed",
    "hours_worked",
    "rating",
    "projects",
    "absences",
]


def load_csv_to_db(csv_path: Path, db_path: Path) -> None:
    """Load employees CSV into a SQLite database.

    Raises:
        FileNotFoundError: if csv_path does not exist.
        ValueError: if required columns are missing from the CSV.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    # normalize date format for SQLite (TEXT)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    with sqlite3.connect(db_path) as con:
        con.execute(SCHEMA_SQL)
        df.to_sql("employees", con, if_exists="replace", index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load employees CSV into SQLite")
    parser.add_argument("--csv", required=True, help="Path to data/employees.csv")
    parser.add_argument("--db", default="hr.db", help="Output SQLite DB path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_csv_to_db(Path(args.csv), Path(args.db))
    print(f"Loaded {args.csv} → {args.db} (table: employees)")


if __name__ == "__main__":
    main()
