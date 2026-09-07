from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.analyze_performance import run_analysis
from src.create_db import load_csv_to_db

REPO_ROOT = Path(__file__).resolve().parents[1]
SQL_PATH = REPO_ROOT / "src" / "queries.sql"


@pytest.fixture
def sample_db(tmp_path: Path, sample_csv: Path) -> Path:
    db_path = tmp_path / "hr.db"
    load_csv_to_db(sample_csv, db_path)
    return db_path


def test_run_analysis_writes_expected_csvs(tmp_path: Path, sample_db: Path) -> None:
    outdir = tmp_path / "outputs"

    run_analysis(sample_db, SQL_PATH, outdir)

    dept_kpis = pd.read_csv(outdir / "department_kpis.csv")
    perf_summary = pd.read_csv(outdir / "performance_summary.csv")

    assert set(dept_kpis["department"]) == {"Engineering", "Sales"}
    assert {"avg_rating", "avg_tasks", "total_hours", "total_tasks", "absence_rate"} <= set(
        dept_kpis.columns
    )
    assert len(perf_summary) == 3  # 3 distinct employees in the fixture
    assert "tasks_per_hour" in perf_summary.columns


def test_run_analysis_writes_charts_by_default(tmp_path: Path, sample_db: Path) -> None:
    outdir = tmp_path / "outputs"

    run_analysis(sample_db, SQL_PATH, outdir)

    charts_dir = outdir / "charts"
    assert (charts_dir / "avg_rating_by_department.png").exists()
    assert (charts_dir / "performance_vs_hours.png").exists()
    assert (charts_dir / "task_completion_rate.png").exists()


def test_run_analysis_no_charts_skips_pngs(tmp_path: Path, sample_db: Path) -> None:
    outdir = tmp_path / "outputs"

    run_analysis(sample_db, SQL_PATH, outdir, make_charts=False)

    assert (outdir / "department_kpis.csv").exists()
    assert not (outdir / "charts").exists() or not any((outdir / "charts").iterdir())


def test_run_analysis_missing_db_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Database not found"):
        run_analysis(tmp_path / "missing.db", SQL_PATH, tmp_path / "out")


def test_run_analysis_missing_sql_raises(tmp_path: Path, sample_db: Path) -> None:
    with pytest.raises(FileNotFoundError, match="SQL file not found"):
        run_analysis(sample_db, tmp_path / "missing.sql", tmp_path / "out")


def test_run_analysis_is_deterministic_for_fixed_seed(tmp_path: Path, sample_db: Path) -> None:
    out_a = tmp_path / "out_a"
    out_b = tmp_path / "out_b"

    run_analysis(sample_db, SQL_PATH, out_a, seed=7)
    run_analysis(sample_db, SQL_PATH, out_b, seed=7)

    a = (out_a / "performance_summary.csv").read_bytes()
    b = (out_b / "performance_summary.csv").read_bytes()
    assert a == b
