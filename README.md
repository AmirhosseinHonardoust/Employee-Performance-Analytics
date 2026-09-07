<div align="center">
 
# Employee Performance Analytics
<img width="1672" height="941" alt="Employee-Performance-Analytics" src="https://github.com/user-attachments/assets/e474de1f-e4a1-4911-ace0-83c0eaf94d65" />

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![pandas](https://img.shields.io/badge/pandas-Data%20Wrangling-orange)
![SQLite](https://img.shields.io/badge/SQLite-KPI%20Aggregation-green)
![Quality Gate](https://img.shields.io/badge/Quality%20Gate-ruff%20%2B%20black%20%2B%20mypy-yellow)
![Status](https://img.shields.io/badge/Status-Portfolio%20Project-purple)
[![CI](https://github.com/AmirhosseinHonardoust/Employee-Performance-Analytics/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/AmirhosseinHonardoust/Employee-Performance-Analytics/actions/workflows/ci.yml)

</div>

A **SQL (SQLite) + Python** analytics pipeline that turns daily employee records into **department KPIs**, **individual performance summaries**, and **productivity charts**, with **data-quality validation**, a **typed and tested codebase**, and **CI-enforced code quality**.

> **Note:** This project uses a **synthetic HR dataset** and is intended as a portfolio / educational demonstration of a SQL + Python analytics workflow.
>
> The KPIs, charts, and insights illustrate how to build a reproducible analytics pipeline; they are not derived from real employee records and should not be used to make actual personnel, compensation, or performance decisions.

---

## Table of Contents

- [Project Overview](#project-overview)
- [What This Project Does](#what-this-project-does)
- [What This Project Does Not Do](#what-this-project-does-not-do)
- [Key Features](#key-features)
- [System Workflow](#system-workflow)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Running the Analysis Pipeline](#running-the-analysis-pipeline)
- [Data Validation](#data-validation)
- [Dataset Description](#dataset-description)
- [SQL Logic](#sql-logic)
- [Visual Reports](#visual-reports)
- [Testing and CI](#testing-and-ci)
- [Code Quality](#code-quality)
- [Limitations](#limitations)
- [Intended Use](#intended-use)
- [Future Improvements](#future-improvements)
- [Tech Stack](#tech-stack)
- [Author](#author)
- [License](#license)

---

## Project Overview

HR analytics is often shown as a single dashboard of numbers without much attention to how those numbers were produced, whether the pipeline is reproducible, or whether the underlying code is tested and typed. This project demonstrates the other half of that picture: a small, honest, end-to-end analytics workflow built the way a production pipeline would be, SQL views for feature engineering, a validated load step, deterministic charts, a typed codebase, a real test suite, and a CI-enforced quality gate.

It uses SQL to compute department- and employee-level KPIs from a daily HR records table, and Python to validate the input data, run the SQL, export CSV reports, and generate charts.

The goal is to show a clean, reproducible SQL + Python analytics workflow end to end, not just a set of charts.

---

## What This Project Does

This project can:

- Load a daily employee-records CSV into a SQLite database
- Validate the data before loading (missing values, out-of-range ratings, invalid absence flags, negative counts)
- Compute department-level KPIs via SQL views (average rating, average tasks, total hours, absence rate)
- Compute per-employee summaries (totals, average rating, efficiency as tasks per hour)
- Compute daily, per-row productivity records
- Export the KPI and summary tables as CSV reports
- Generate three charts: average rating by department, performance vs. hours worked, and task-completion-rate distribution
- Regenerate charts deterministically via a fixed random seed
- Run automated tests with coverage reporting, and a GitHub Actions CI quality gate

---

## What This Project Does Not Do

This project does **not**:

- Predict future performance, attrition, or turnover
- Run statistical significance testing on department differences
- Detect anomalies or outliers automatically
- Provide a web dashboard or UI (it is a CLI + SQL pipeline)
- Work with real, sensitive, or personally identifiable employee data, the bundled dataset is synthetic
- Replace an actual HR analytics or BI platform

---

## Key Features

- **SQL views** (`src/queries.sql`) for department, employee, and daily-level KPI aggregation
- **Data-quality validation** before load: null checks, rating range, absences domain, non-negative counts
- **Deterministic chart generation** via a `--seed` flag for reproducible scatter sampling
- **Typed Python codebase** (`from __future__ import annotations`), clean under `mypy`
- **Unit test suite** with coverage reporting (`pytest` + `pytest-cov`)
- **GitHub Actions CI** matrix across Python 3.10 and 3.12, plus an end-to-end pipeline smoke test
- **Dependabot**-managed dependency updates and an advisory `pip-audit` scan
- **CLI polish**: `--version` on both entry points, environment-variable-driven path defaults
- **Single-source dependency management** via `pyproject.toml`

---

## System Workflow

```text
employees.csv
        ↓
create_db.py (validate + load)
        ↓
SQLite "employees" table
        ↓
queries.sql (department_kpis / employee_summary / daily_productivity views)
        ↓
analyze_performance.py
        ↓
department_kpis.csv + performance_summary.csv
        ↓
charts (bar / scatter / histogram)
```

---

## Project Structure

```text
Employee-Performance-Analytics/
│
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       └── ci.yml
│
├── data/
│   └── employees.csv
│
├── outputs/
│   ├── charts/
│   │   ├── avg_rating_by_department.png
│   │   ├── performance_vs_hours.png
│   │   └── task_completion_rate.png
│   ├── department_kpis.csv
│   └── performance_summary.csv
│
├── src/
│   ├── __init__.py
│   ├── create_db.py
│   ├── analyze_performance.py
│   ├── queries.sql
│   └── utils.py
│
├── tests/
│   ├── conftest.py
│   ├── test_analyze_performance.py
│   ├── test_cli.py
│   ├── test_create_db.py
│   └── test_utils.py
│
├── .gitattributes
├── .gitignore
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
└── requirements.txt
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AmirhosseinHonardoust/Employee-Performance-Analytics.git
cd Employee-Performance-Analytics
```

### 2. Create a Virtual Environment

On Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Dependency versions are declared once, in `pyproject.toml`. Either of these works:

```bash
pip install -r requirements.txt
```

```bash
pip install -e .
```

For development tools (pytest, ruff, black, mypy):

```bash
pip install -e ".[dev]"
```

---

## Quick Start

Load data into SQLite:

```bash
python src/create_db.py --csv data/employees.csv --db hr.db
```

Run the analysis:

```bash
python src/analyze_performance.py --db hr.db --sql src/queries.sql --outdir outputs
```

All CSV reports and charts are saved to the `outputs/` directory.

---

## Running the Analysis Pipeline

The scripts also work as package modules (`python -m src.create_db ...`, `python -m src.analyze_performance ...`), which is what the test suite and CI exercise indirectly by importing `src`.

Useful flags:

- `--seed <int>` on `analyze_performance.py` | random seed for the scatter-plot sample (default `42`, for reproducible charts)
- `--no-charts` on `analyze_performance.py` | skip PNG generation and only write the summary CSVs (faster for CI or quick checks)
- `--version` on both scripts | print the installed package version
- `EMP_DB_PATH` / `EMP_OUTDIR` environment variables | override the default DB and output-directory paths on both scripts

```bash
python src/analyze_performance.py --db hr.db --sql src/queries.sql --outdir outputs --seed 7 --no-charts
```

Generated outputs include:

```text
outputs/department_kpis.csv
outputs/performance_summary.csv
outputs/charts/avg_rating_by_department.png
outputs/charts/performance_vs_hours.png
outputs/charts/task_completion_rate.png
```

---

## Data Validation

Before a CSV is loaded into SQLite, `create_db.py` validates it (`validate_employees_df`):

<div align="center">

| Check | Rule |
|---|---|
| Missing values | No nulls in any required column |
| `rating` | Must fall within 0–5 |
| `absences` | Must be `0` or `1` |
| `tasks_completed`, `hours_worked`, `projects` | Must be non-negative |

</div>

A failing row raises a `ValueError` with a specific message (e.g. `"CSV has 'rating' values outside the expected 0-5 range"`) instead of silently propagating bad data into the KPI calculations.

> The bundled `data/employees.csv` passes all of these checks. The validation exists to catch bad data early, not because the shipped dataset has any known issues.

---

## Dataset Description
<div align="center">

| Column | Description |
|---|---|
| `employee_id` | Unique employee identifier |
| `name` | Employee name |
| `department` | Department name (Engineering, Sales, etc.) |
| `role` | Role title |
| `date` | Record date (YYYY-MM-DD) |
| `tasks_completed` | Number of tasks completed |
| `hours_worked` | Hours worked on that day |
| `rating` | Daily performance rating (0–5) |
| `projects` | Active projects |
| `absences` | 1 if absent, else 0 |

</div>

> The dataset (`employees.csv`) is synthetic, generated with realistic departmental trends and biases.

---

## SQL Logic

`src/queries.sql` creates three temp views, each consumed separately by `analyze_performance.py` via `pd.read_sql_query()`:

<div align="center">

| View | Purpose |
|---|---|
| `department_kpis` | Average rating, average tasks, total hours, total tasks, and absence rate per department |
| `employee_summary` | Per-employee totals (tasks, hours, projects, absences), average rating, and tasks-per-hour efficiency |
| `daily_productivity` | Per-row daily workload and tasks-per-hour |

</div>

> The file also contains three standalone `SELECT` statements after the views. These are for manual inspection only (e.g. running the file directly via the `sqlite3` CLI), `analyze_performance.py` runs the whole script with `executescript()`, which creates the views but discards those `SELECT` results, then queries each view itself.

---

## Visual Reports

<div align="center">

| Average Rating by Department | Performance vs. Hours Worked |
|---|---|
| <img width="380" alt="Average rating by department" src="https://github.com/user-attachments/assets/6b5666ae-d7ed-4a56-948b-2944122a24e0" /> | <img width="380" alt="Performance vs hours" src="https://github.com/user-attachments/assets/b894b553-2adc-4373-9583-f531b10efbbe" /> |
| **Analysis:** Clear variation between departments (Finance and Engineering higher, Support and Sales lower), suggesting differences in consistency or performance culture. | **Analysis:** Higher hours correlate with more tasks completed up to a plateau; clusters show standard workloads, and outliers can reveal inefficiency or exceptional performers. |

</div>

<details>
<summary>Additional chart: task completion rate distribution</summary>

<div align="center">
        
| Task Completion Rate Distribution |
|---|
| <img width="600" alt="Task completion rate distribution" src="https://github.com/user-attachments/assets/a4f5dd3b-4179-49e6-a921-6bc75a8083d7" /> |
| Most employees average around 1 task/hour; high performers exceed 1.4 and low performers fall under 0.8, useful for spotting training needs or recognizing excellence. |

</div>

</details>

---

## Testing and CI

Run the full quality gate locally:

```bash
ruff check src/ tests/
black --check src/ tests/
mypy src/
pytest tests/ --cov=src --cov-report=term-missing
```

The GitHub Actions workflow checks:

- dependency installation (`pip install -e ".[dev]"`)
- linting with Ruff
- formatting with Black
- type checking with mypy
- unit tests with coverage reporting
- an end-to-end pipeline smoke test (`create_db.py` → `analyze_performance.py`) on Python 3.10 and 3.12
- an advisory, non-blocking `pip-audit` dependency scan

CI is defined in:

```text
.github/workflows/ci.yml
```

---

## Code Quality

<div align="center">

| Module | Purpose |
|---|---|
| `src/create_db.py` | CSV validation and loading into SQLite |
| `src/queries.sql` | SQL views for KPI and productivity aggregation |
| `src/analyze_performance.py` | Runs the SQL, exports CSV reports, generates charts |
| `src/utils.py` | Shared helpers: output-dir handling, CSV saving, chart plotting, version/logging helpers |

</div>

Tooling is configured through `pyproject.toml` (ruff, black, mypy, pytest, coverage) and enforced identically in CI.

---

## Limitations

This project has important limitations:

- The dataset is a small, synthetic snapshot, not real organizational data
- No statistical testing is performed on department- or employee-level differences
- Charts use matplotlib defaults with no interactivity
- There is no anomaly, outlier, or trend-over-time detection
- The pipeline assumes a single flat CSV source, not incremental or streaming updates
- Data-quality validation covers structural correctness, not semantic correctness (e.g. it cannot detect a mislabeled department)

The project is strongest as a portfolio demonstration of a clean, tested, reproducible SQL + Python analytics workflow.

---

## Intended Use

This repository is intended for:

- SQL and Python analytics education
- practicing reproducible, tested data pipelines
- demonstrating a CI-enforced quality gate on a small codebase
- portfolio demonstration

It should not be used as-is for:

- real personnel, compensation, or promotion decisions
- performance reviews without human oversight
- any high-stakes HR or compliance decision

Any real deployment would require real (and properly governed) HR data, statistical validation, and human review.

---

## Future Improvements

Potential next improvements:

- Add time-series / trend analysis across multiple periods
- Add anomaly or outlier detection for daily productivity records
- Enforce a coverage threshold in CI rather than reporting only
- Add a dependency lockfile for fully reproducible installs
- Add a lightweight dashboard for interactive KPI browsing
- Add duplicate-row detection to the validation step
- Add Docker packaging for the pipeline

---

## Tech Stack

- Python
- pandas
- SQLite
- matplotlib
- pytest / pytest-cov
- ruff
- black
- mypy
- GitHub Actions
- Dependabot

---

## Author

**Amir Honardoust**

GitHub: [@AmirhosseinHonardoust](https://github.com/AmirhosseinHonardoust)

---

## License

Licensed under the **MIT License**, see [LICENSE](LICENSE) for the full text.

This project is intended for educational, research, and portfolio purposes.
