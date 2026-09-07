# Changelog

All notable changes to this project are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Row-level data validation in `create_db.py` (null checks, rating range,
  absences domain, non-negative counts) with matching tests.
- Test coverage reporting via `pytest-cov`, wired into CI.
- `--version` flag on both CLI entry points.
- Env-driven defaults for DB/output paths (`EMP_DB_PATH`, `EMP_OUTDIR`).
- `.gitattributes` to enforce LF line endings for text files.
- Dependabot config (pip + GitHub Actions) and an advisory, non-blocking
  `pip-audit` CI step.
- `CONTRIBUTING.md`.

### Changed
- `requirements.txt` now installs the package in editable mode
  (`-e .`) instead of duplicating version pins already declared in
  `pyproject.toml`.
- CLI status messages now go through `logging` instead of bare `print`.
- Regenerated committed CSV outputs with LF line endings (content unchanged).

## [0.1.0] - prior to this changelog
- Initial SQL + Python employee performance analytics pipeline.
- Quality gate (ruff, black, mypy), test suite, and CI (#1).
