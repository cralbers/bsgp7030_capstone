"""AgGrid row and column builders for stadium and coach tables."""

from __future__ import annotations

from config import RATE_OPTIONS
from data import load_coach_win_rates, load_stadium_win_rates


def build_top_stadiums_rows(rate_mode: str) -> list[dict]:
    """Return stadiums sorted by the selected win rate (highest first)."""
    df = load_stadium_win_rates()
    meta = RATE_OPTIONS.get(rate_mode, RATE_OPTIONS["home"])
    rate_col = meta["column"]
    table = (
        df[["Stadium", "City", "matches", rate_col]]
        .sort_values(rate_col, ascending=False)
        .copy()
    )
    table[rate_col] = table[rate_col].round(1)
    return table.to_dict("records")


def build_top_stadiums_column_defs(rate_mode: str) -> list[dict]:
    """Column definitions for the top-stadiums AgGrid."""
    meta = RATE_OPTIONS.get(rate_mode, RATE_OPTIONS["home"])
    rate_col = meta["column"]
    return [
        {"field": "Stadium", "headerName": "Stadium"},
        {"field": "City", "headerName": "City"},
        {"field": "matches", "headerName": "Matches"},
        {"field": rate_col, "headerName": meta["rate_header"]},
    ]


def build_coach_rows() -> list[dict]:
    """Return coaches sorted by total matches (highest first)."""
    df = load_coach_win_rates()
    table = (
        df[
            [
                "Coach Name",
                "home_matches",
                "home_win_rate",
                "away_matches",
                "away_win_rate",
                "total_matches",
            ]
        ]
        .sort_values("total_matches", ascending=False)
        .copy()
    )
    table["home_win_rate"] = table["home_win_rate"].round(1)
    table["away_win_rate"] = table["away_win_rate"].round(1)
    return table.to_dict("records")


def build_coach_column_defs() -> list[dict]:
    """Column definitions for the coaches AgGrid."""
    return [
        {"field": "Coach Name", "headerName": "Coach"},
        {"field": "home_matches", "headerName": "Home matches"},
        {"field": "home_win_rate", "headerName": "Home win rate (%)"},
        {"field": "away_matches", "headerName": "Away matches"},
        {"field": "away_win_rate", "headerName": "Away win rate (%)"},
        {"field": "total_matches", "headerName": "Total matches"},
    ]
