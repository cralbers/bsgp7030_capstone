"""Cached CSV loaders with schema validation and view filters."""

from __future__ import annotations

import pandas as pd

from config import COACH_CSV_PATH, CSV_PATH, DEFAULT_MIN_MATCHES, YEAR_MAX, YEAR_MIN
from schema import validate_coach_df, validate_stadium_df

_stadium_loader = None
_coach_loader = None


def init_cache(cache) -> None:
    """Wire flask-caching memoize onto the CSV loaders."""
    global _stadium_loader, _coach_loader

    @cache.memoize()
    def _load_stadium_win_rates() -> pd.DataFrame:
        return validate_stadium_df(pd.read_csv(CSV_PATH))

    @cache.memoize()
    def _load_coach_win_rates() -> pd.DataFrame:
        return validate_coach_df(pd.read_csv(COACH_CSV_PATH))

    _stadium_loader = _load_stadium_win_rates
    _coach_loader = _load_coach_win_rates


def load_stadium_win_rates() -> pd.DataFrame:
    """Load precomputed stadium win rates and coordinates."""
    if _stadium_loader is None:
        raise RuntimeError("Call data.init_cache(cache) before loading CSVs")
    return _stadium_loader()


def load_coach_win_rates() -> pd.DataFrame:
    """Load precomputed coach home/away win rates."""
    if _coach_loader is None:
        raise RuntimeError("Call data.init_cache(cache) before loading CSVs")
    return _coach_loader()


def _year_overlap_mask(
    df: pd.DataFrame,
    year_start: int,
    year_end: int,
) -> pd.Series:
    """True where entity year span overlaps [year_start, year_end]."""
    if "year_min" not in df.columns or "year_max" not in df.columns:
        return pd.Series(True, index=df.index)
    return (df["year_max"] >= year_start) & (df["year_min"] <= year_end)


def filter_stadiums(
    df: pd.DataFrame | None = None,
    *,
    min_matches: int = DEFAULT_MIN_MATCHES,
    year_start: int = YEAR_MIN,
    year_end: int = YEAR_MAX,
) -> pd.DataFrame:
    """Filter stadiums by minimum matches and year-span overlap."""
    out = load_stadium_win_rates() if df is None else df.copy()
    out = out[out["matches"] >= min_matches]
    out = out[_year_overlap_mask(out, year_start, year_end)]
    return out.reset_index(drop=True)


def filter_coaches(
    df: pd.DataFrame | None = None,
    *,
    min_matches: int = DEFAULT_MIN_MATCHES,
    year_start: int = YEAR_MIN,
    year_end: int = YEAR_MAX,
) -> pd.DataFrame:
    """Filter coaches by min home and away matches and year-span overlap."""
    out = load_coach_win_rates() if df is None else df.copy()
    out = out[
        (out["home_matches"] >= min_matches) & (out["away_matches"] >= min_matches)
    ]
    out = out[_year_overlap_mask(out, year_start, year_end)]
    return out.reset_index(drop=True)
