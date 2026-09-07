from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils import ensure_outdir, get_version, plot_bar, plot_hist, plot_scatter, save_csv


def test_get_version_returns_nonempty_string() -> None:
    assert isinstance(get_version(), str)
    assert get_version() != ""


def test_ensure_outdir_creates_nested_dirs(tmp_path: Path) -> None:
    target = tmp_path / "a" / "b" / "c"
    result = ensure_outdir(target)
    assert result == target
    assert target.is_dir()


def test_ensure_outdir_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "existing"
    target.mkdir()
    result = ensure_outdir(target)
    assert result == target


def test_save_csv_writes_expected_content(tmp_path: Path) -> None:
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    out_path = tmp_path / "nested" / "out.csv"

    result = save_csv(df, out_path)

    assert result == out_path
    assert out_path.exists()
    loaded = pd.read_csv(out_path)
    pd.testing.assert_frame_equal(loaded, df)


def test_plot_bar_creates_png(tmp_path: Path) -> None:
    df = pd.DataFrame({"dept": ["A", "B"], "rating": [3.5, 4.1]})
    out_path = tmp_path / "bar.png"

    result = plot_bar(df, x="dept", y="rating", title="t", out_path=out_path)

    assert result == out_path
    assert out_path.exists()
    assert out_path.stat().st_size > 0


def test_plot_scatter_creates_png(tmp_path: Path) -> None:
    df = pd.DataFrame({"hours": [1.0, 2.0, 3.0], "tasks": [1, 2, 3]})
    out_path = tmp_path / "scatter.png"

    result = plot_scatter(df, x="hours", y="tasks", title="t", out_path=out_path)

    assert result == out_path
    assert out_path.exists()


def test_plot_hist_creates_png(tmp_path: Path) -> None:
    series = pd.Series([1.0, 2.0, 2.0, 3.0])
    out_path = tmp_path / "hist.png"

    result = plot_hist(series, title="t", out_path=out_path)

    assert result == out_path
    assert out_path.exists()
