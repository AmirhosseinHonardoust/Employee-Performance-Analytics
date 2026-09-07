from __future__ import annotations

import logging
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PathLike = str | Path

_DIST_NAME = "employee-performance-analytics"


def get_version() -> str:
    """Return the installed package version, or 'unknown' if not installed."""
    try:
        return version(_DIST_NAME)
    except PackageNotFoundError:  # pragma: no cover - only hit outside an install
        return "unknown"


def configure_logging() -> logging.Logger:
    """Configure a plain, message-only logger shared by the CLI entry points."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    return logging.getLogger("employee_performance_analytics")


def ensure_outdir(path: PathLike) -> Path:
    """Create directory if it doesn't exist and return it as Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_csv(df: pd.DataFrame, path: PathLike, index: bool = False) -> Path:
    """Save DataFrame to CSV ensuring parent directory exists."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=index)
    return out


def plot_bar(df: pd.DataFrame, x: str, y: str, title: str, out_path: PathLike) -> Path:
    """Simple bar plot (Matplotlib defaults)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df[x], df[y])
    ax.set_title(title)
    ax.set_xlabel(x.replace("_", " ").title())
    ax.set_ylabel(y.replace("_", " ").title())
    plt.xticks(rotation=30, ha="right")
    out = Path(out_path)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_scatter(df: pd.DataFrame, x: str, y: str, title: str, out_path: PathLike) -> Path:
    """Simple scatter plot (Matplotlib defaults)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df[x], df[y])
    ax.set_title(title)
    ax.set_xlabel(x.replace("_", " ").title())
    ax.set_ylabel(y.replace("_", " ").title())
    out = Path(out_path)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_hist(series: pd.Series, title: str, out_path: PathLike) -> Path:
    """Histogram for a numeric series (Matplotlib defaults)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(series, bins=30)
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    out = Path(out_path)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out
