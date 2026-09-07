#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sqlite3
from pathlib import Path

import pandas as pd

try:
    from .utils import configure_logging, get_version
except ImportError:  # pragma: no cover - fallback when run as a bare script
    from utils import configure_logging, get_version  # type: ignore[import-not-found,no-redef]

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


def validate_employees_df(df: pd.DataFrame) -> None:
    """Validate row-level data quality beyond column presence.

    Raises:
        ValueError: if required columns contain nulls or out-of-range values.
    """
    null_counts = df[REQUIRED_COLUMNS].isnull().sum()
    bad_cols = null_counts[null_counts > 0]
    if not bad_cols.empty:
        raise ValueError(f"CSV has null values in required columns: {bad_cols.to_dict()}")

    if not df["rating"].between(0, 5).all():
        raise ValueError("CSV has 'rating' values outside the expected 0-5 range")

    if not df["absences"].isin([0, 1]).all():
        raise ValueError("CSV has 'absences' values other than 0 or 1")

    for col in ("tasks_completed", "hours_worked", "projects"):
        if (df[col] < 0).any():
            raise ValueError(f"CSV has negative values in '{col}'")


def load_csv_to_db(csv_path: Path, db_path: Path) -> None:
    """Load employees CSV into a SQLite database.

    Raises:
        FileNotFoundError: if csv_path does not exist.
        ValueError: if required columns are missing, or row values fail validation.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    validate_employees_df(df)

    # normalize date format for SQLite (TEXT)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    with sqlite3.connect(db_path) as con:
        con.execute(SCHEMA_SQL)
        df.to_sql("employees", con, if_exists="replace", index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load employees CSV into SQLite")
    parser.add_argument("--version", action="version", version=get_version())
    parser.add_argument("--csv", required=True, help="Path to data/employees.csv")
    parser.add_argument(
        "--db",
        default=os.environ.get("EMP_DB_PATH", "hr.db"),
        help="Output SQLite DB path (env: EMP_DB_PATH)",
    )
    return parser.parse_args()


def main() -> None:
    logger = configure_logging()
    args = parse_args()
    load_csv_to_db(Path(args.csv), Path(args.db))
    logger.info("Loaded %s → %s (table: employees)", args.csv, args.db)


if __name__ == "__main__":
    main()
