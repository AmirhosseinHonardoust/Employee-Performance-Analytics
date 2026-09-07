# Contributing

Thanks for considering a contribution! This is a small project, so the process is simple.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

## Before opening a PR

Run the full quality gate locally — this is exactly what CI runs:

```bash
ruff check src/ tests/
black --check src/ tests/
mypy src/
pytest tests/ -v --cov=src --cov-report=term-missing
```

If you touch `src/create_db.py` or `src/analyze_performance.py`, also run the
end-to-end pipeline once to sanity-check real output:

```bash
python src/create_db.py --csv data/employees.csv --db hr.db
python src/analyze_performance.py --db hr.db --sql src/queries.sql --outdir outputs
```

## Conventions

- Keep changes minimal and focused; avoid unrelated renames or file moves.
- Match existing patterns (type hints via `from __future__ import annotations`,
  the package/bare-script import fallback in `src/analyze_performance.py` and
  `src/create_db.py`, `pathlib.Path` over raw strings).
- Add or update tests for any behavior change.
- For refactors, show that output is unchanged (e.g. diff generated CSVs
  before/after).

## Reporting issues

Open a GitHub issue with steps to reproduce, expected vs. actual behavior,
and your Python version.
