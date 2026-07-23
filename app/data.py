"""Cached CSV loaders with schema validation."""

from __future__ import annotations

import pandas as pd

from config import COACH_CSV_PATH, CSV_PATH
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
