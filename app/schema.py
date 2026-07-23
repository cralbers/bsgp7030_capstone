"""CSV schema contracts and light validation for app loaders."""

from __future__ import annotations

import pandas as pd

STADIUM_REQUIRED_COLUMNS = (
    "Stadium",
    "City",
    "matches",
    "home_win_rate",
    "away_win_rate",
    "lat",
    "lon",
)

COACH_REQUIRED_COLUMNS = (
    "Coach Name",
    "home_matches",
    "home_wins",
    "home_win_rate",
    "away_matches",
    "away_wins",
    "away_win_rate",
    "total_matches",
)


def _require_columns(df: pd.DataFrame, required: tuple[str, ...], label: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{label} CSV missing columns: {missing}")


def validate_stadium_df(df: pd.DataFrame) -> pd.DataFrame:
    """Validate stadium CSV columns; soft-drop rows with null lat/lon."""
    _require_columns(df, STADIUM_REQUIRED_COLUMNS, "Stadium")
    out = df.copy()
    before = len(out)
    out = out.dropna(subset=["lat", "lon"]).reset_index(drop=True)
    dropped = before - len(out)
    if dropped:
        print(f"Dropped {dropped} stadium row(s) with null lat/lon")
    return out


def validate_coach_df(df: pd.DataFrame) -> pd.DataFrame:
    """Validate coach CSV columns; return a copy."""
    _require_columns(df, COACH_REQUIRED_COLUMNS, "Coach")
    return df.copy()
