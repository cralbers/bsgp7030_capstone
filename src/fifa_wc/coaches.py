"""Coach home/away win-rate aggregation."""

from __future__ import annotations

import pandas as pd

from fifa_wc.config import MIN_COACH_AWAY, MIN_COACH_HOME
from fifa_wc.outcomes import clean_matches_for_coaches


def aggregate_coach_rates(
    matches_df: pd.DataFrame,
    players_df: pd.DataFrame,
    min_home: int = MIN_COACH_HOME,
    min_away: int = MIN_COACH_AWAY,
) -> pd.DataFrame:
    """Join coaches onto matches and aggregate home/away win rates."""
    coaches = (
        players_df[["MatchID", "Team Initials", "Coach Name"]]
        .dropna(subset=["Coach Name", "MatchID", "Team Initials"])
        .drop_duplicates()
    )

    m_coach = clean_matches_for_coaches(matches_df)

    home_coach = m_coach.merge(
        coaches,
        left_on=["MatchID", "Home Team Initials"],
        right_on=["MatchID", "Team Initials"],
        how="inner",
    )
    away_coach = m_coach.merge(
        coaches,
        left_on=["MatchID", "Away Team Initials"],
        right_on=["MatchID", "Team Initials"],
        how="inner",
    )

    home_coach["win"] = (
        home_coach["Home Team Goals"] > home_coach["Away Team Goals"]
    ).astype(int)
    away_coach["win"] = (
        away_coach["Away Team Goals"] > away_coach["Home Team Goals"]
    ).astype(int)

    home_agg_kwargs = dict(
        home_matches=("win", "size"),
        home_wins=("win", "sum"),
    )
    away_agg_kwargs = dict(
        away_matches=("win", "size"),
        away_wins=("win", "sum"),
    )
    if "Year" in home_coach.columns:
        home_agg_kwargs["home_year_min"] = ("Year", "min")
        home_agg_kwargs["home_year_max"] = ("Year", "max")
    if "Year" in away_coach.columns:
        away_agg_kwargs["away_year_min"] = ("Year", "min")
        away_agg_kwargs["away_year_max"] = ("Year", "max")

    home_agg = home_coach.groupby("Coach Name", as_index=False).agg(**home_agg_kwargs)
    away_agg = away_coach.groupby("Coach Name", as_index=False).agg(**away_agg_kwargs)

    coach_rates = home_agg.merge(away_agg, on="Coach Name", how="inner")
    coach_rates = coach_rates[
        (coach_rates["home_matches"] >= min_home)
        & (coach_rates["away_matches"] >= min_away)
    ].copy()
    coach_rates["home_win_rate"] = (
        100 * coach_rates["home_wins"] / coach_rates["home_matches"]
    )
    coach_rates["away_win_rate"] = (
        100 * coach_rates["away_wins"] / coach_rates["away_matches"]
    )
    coach_rates["total_matches"] = (
        coach_rates["home_matches"] + coach_rates["away_matches"]
    )
    if "home_year_min" in coach_rates.columns:
        coach_rates["year_min"] = coach_rates[
            ["home_year_min", "away_year_min"]
        ].min(axis=1)
        coach_rates["year_max"] = coach_rates[
            ["home_year_max", "away_year_max"]
        ].max(axis=1)
        coach_rates = coach_rates.drop(
            columns=[
                "home_year_min",
                "home_year_max",
                "away_year_min",
                "away_year_max",
            ]
        )
    return coach_rates.sort_values("total_matches", ascending=False).reset_index(
        drop=True
    )


COACH_EXPORT_COLUMNS = [
    "Coach Name",
    "home_matches",
    "home_wins",
    "home_win_rate",
    "away_matches",
    "away_wins",
    "away_win_rate",
    "total_matches",
    "year_min",
    "year_max",
]
