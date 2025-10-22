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


def load_csv_to_db(csv_path: Path, db_path: Path) -> None:
    """Load employees CSV into a SQLite database."""
    df = pd.read_csv(csv_path, parse_dates=["date"])
    # normalize date format for SQLite (TEXT)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

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
