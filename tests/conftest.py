from __future__ import annotations

from pathlib import Path

import pytest

_HEADER = (
    "employee_id,name,department,role,date," "tasks_completed,hours_worked,rating,projects,absences"
)
_ROWS = [
    "E1,Alice,Engineering,Dev,2024-01-01,8,7.0,4.2,1,0",
    "E1,Alice,Engineering,Dev,2024-01-02,6,6.5,3.8,1,0",
    "E2,Bob,Sales,Rep,2024-01-01,10,8.0,3.1,2,1",
    "E2,Bob,Sales,Rep,2024-01-02,9,7.5,3.4,2,0",
    "E3,Carol,Engineering,Lead,2024-01-01,4,5.0,4.9,0,0",
]
SAMPLE_CSV_ROWS = "\n".join([_HEADER, *_ROWS]) + "\n"


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """A small, deterministic synthetic employees CSV for tests."""
    csv_path = tmp_path / "employees.csv"
    csv_path.write_text(SAMPLE_CSV_ROWS, encoding="utf-8")
    return csv_path
