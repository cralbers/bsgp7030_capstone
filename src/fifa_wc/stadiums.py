"""Stadium home/away/draw win-rate aggregation."""

from __future__ import annotations

import pandas as pd

from fifa_wc.config import MIN_STADIUM_MATCHES
from fifa_wc.outcomes import clean_matches_for_stadiums


def aggregate_stadium_rates(matches_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate home/away/draw rates (%) by stadium."""
    m = clean_matches_for_stadiums(matches_df)
    stadium_rates = (
        m.groupby("Stadium", as_index=False)
        .agg(
            City=("City", "first"),
            matches=("home_win", "size"),
            home_win_rate=("home_win", "mean"),
            away_win_rate=("away_win", "mean"),
            draw_rate=("draw", "mean"),
        )
        .sort_values("matches", ascending=False)
    )
    stadium_rates["home_win_rate"] *= 100
    stadium_rates["away_win_rate"] *= 100
    stadium_rates["draw_rate"] *= 100
    return stadium_rates.reset_index(drop=True)


def filter_stadiums_for_map(
    stadium_rates: pd.DataFrame,
    min_matches: int = MIN_STADIUM_MATCHES,
) -> pd.DataFrame:
    """Keep stadiums with enough matches for stable map rates."""
    return stadium_rates[stadium_rates["matches"] >= min_matches].copy()
