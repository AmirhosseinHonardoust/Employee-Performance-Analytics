#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

try:
    from .utils import ensure_outdir, plot_bar, plot_hist, plot_scatter, save_csv
except ImportError:  # pragma: no cover - fallback when run as a bare script
    from utils import (  # type: ignore[import-not-found,no-redef]
        ensure_outdir,
        plot_bar,
        plot_hist,
        plot_scatter,
        save_csv,
    )


def run_analysis(
    db_path: Path,
    sql_path: Path,
    outdir: Path,
    seed: int = 42,
    make_charts: bool = True,
) -> None:
    """Execute SQL feature engineering (via executescript), export CSVs and charts.

    Raises:
        FileNotFoundError: if db_path or sql_path do not exist.
    """
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path} (run src/create_db.py first)")
    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    outdir = ensure_outdir(outdir)
    charts_dir = ensure_outdir(outdir / "charts") if make_charts else outdir / "charts"

    # Read full SQL; we'll exec the script (it can include CREATE VIEWs and SELECTs).
    sql_text = sql_path.read_text(encoding="utf-8")

    with sqlite3.connect(db_path) as con:
        # Create views / temp objects etc. (SELECT outputs are ignored here)
        con.executescript(sql_text)

        # Now fetch the three result tables explicitly (robust to file formatting)
        dept_kpis = pd.read_sql_query(
            "SELECT * FROM department_kpis ORDER BY avg_rating DESC;", con
        )
        emp_summary = pd.read_sql_query(
            "SELECT * FROM employee_summary ORDER BY tasks_per_hour DESC;", con
        )
        daily_prod = pd.read_sql_query("SELECT * FROM daily_productivity;", con)

    # Save CSVs
    save_csv(dept_kpis, outdir / "department_kpis.csv")
    save_csv(emp_summary, outdir / "performance_summary.csv")

    if not make_charts:
        print(f"Artifacts saved to: {outdir.resolve()} (charts skipped)")
        return

    # Charts
    if not dept_kpis.empty:
        plot_bar(
            dept_kpis,
            x="department",
            y="avg_rating",
            title="Average Rating by Department",
            out_path=charts_dir / "avg_rating_by_department.png",
        )

    if not daily_prod.empty:
        sample = daily_prod.sample(n=min(5000, len(daily_prod)), random_state=seed)
        plot_scatter(
            sample,
            x="hours_worked",
            y="tasks_completed",
            title="Performance vs Hours (Daily Tasks vs Hours)",
            out_path=charts_dir / "performance_vs_hours.png",
        )

    if not emp_summary.empty:
        plot_hist(
            emp_summary["tasks_per_hour"].fillna(0),
            title="Task Completion Rate (Tasks per Hour)",
            out_path=charts_dir / "task_completion_rate.png",
        )

    print(f"Artifacts saved to: {outdir.resolve()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Employee performance analytics (SQL + Python)")
    parser.add_argument("--db", default="hr.db", help="Path to SQLite DB")
    parser.add_argument("--sql", default="src/queries.sql", help="Path to queries.sql")
    parser.add_argument("--outdir", default="outputs", help="Output directory")
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for chart sampling (default: 42)",
    )
    parser.add_argument(
        "--no-charts",
        action="store_true",
        help="Skip chart generation and only write summary CSVs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_analysis(
        Path(args.db),
        Path(args.sql),
        Path(args.outdir),
        seed=args.seed,
        make_charts=not args.no_charts,
    )


if __name__ == "__main__":
    main()
