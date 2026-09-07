from __future__ import annotations

import sys

from src.analyze_performance import parse_args as analyze_parse_args
from src.create_db import parse_args as create_db_parse_args


def test_create_db_version_flag_exits_zero(capsys) -> None:  # type: ignore[no-untyped-def]
    old_argv = sys.argv
    try:
        sys.argv = ["create_db.py", "--version"]
        try:
            create_db_parse_args()
        except SystemExit as exc:
            assert exc.code == 0
    finally:
        sys.argv = old_argv


def test_analyze_performance_version_flag_exits_zero(capsys) -> None:  # type: ignore[no-untyped-def]
    old_argv = sys.argv
    try:
        sys.argv = ["analyze_performance.py", "--version"]
        try:
            analyze_parse_args()
        except SystemExit as exc:
            assert exc.code == 0
    finally:
        sys.argv = old_argv


def test_create_db_db_default_reads_env(monkeypatch) -> None:  # type: ignore[no-untyped-def]

    monkeypatch.setenv("EMP_DB_PATH", "env_hr.db")
    old_argv = sys.argv
    try:
        sys.argv = ["create_db.py", "--csv", "data/employees.csv"]
        args = create_db_parse_args()
        assert args.db == "env_hr.db"
    finally:
        sys.argv = old_argv


def test_analyze_performance_outdir_default_reads_env(monkeypatch) -> None:  # type: ignore[no-untyped-def]

    monkeypatch.setenv("EMP_OUTDIR", "env_outputs")
    old_argv = sys.argv
    try:
        sys.argv = ["analyze_performance.py"]
        args = analyze_parse_args()
        assert args.outdir == "env_outputs"
    finally:
        sys.argv = old_argv


def test_env_vars_unset_fall_back_to_defaults(monkeypatch) -> None:  # type: ignore[no-untyped-def]

    monkeypatch.delenv("EMP_DB_PATH", raising=False)
    monkeypatch.delenv("EMP_OUTDIR", raising=False)
    old_argv = sys.argv
    try:
        sys.argv = ["create_db.py", "--csv", "data/employees.csv"]
        assert create_db_parse_args().db == "hr.db"

        sys.argv = ["analyze_performance.py"]
        args = analyze_parse_args()
        assert args.db == "hr.db"
        assert args.outdir == "outputs"
    finally:
        sys.argv = old_argv
