#!/usr/bin/env python3
"""Build app/stadium_win_rates.csv and app/coach_win_rates.csv from raw World Cup data.

Prefer local files under data/ when present; otherwise load via kagglehub.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from fifa_wc.coaches import COACH_EXPORT_COLUMNS, aggregate_coach_rates
from fifa_wc.config import (
    COACH_CSV_PATH,
    KAGGLE_DATASET,
    MATCHES_CSV,
    PLAYERS_CSV,
    STADIUM_CSV_PATH,
)
from fifa_wc.geocode import geocode_stadiums
from fifa_wc.stadiums import aggregate_stadium_rates, filter_stadiums_for_map


STADIUM_EXPORT_COLUMNS = [
    "Stadium",
    "City",
    "matches",
    "home_win_rate",
    "away_win_rate",
    "draw_rate",
    "year_min",
    "year_max",
    "lat",
    "lon",
]


def load_raw_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load matches and players from local CSVs or Kaggle."""
    if MATCHES_CSV.exists() and PLAYERS_CSV.exists():
        print(f"Loading local CSVs from {MATCHES_CSV.parent}")
        matches_df = pd.read_csv(MATCHES_CSV, encoding="utf-8")
        players_df = pd.read_csv(PLAYERS_CSV, encoding="utf-8")
        return matches_df, players_df

    print(f"Local data not found; loading via kagglehub ({KAGGLE_DATASET})")
    import kagglehub
    from kagglehub import KaggleDatasetAdapter

    matches_df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        KAGGLE_DATASET,
        "WorldCupMatches.csv",
    )
    players_df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        KAGGLE_DATASET,
        "WorldCupPlayers.csv",
    )
    return matches_df, players_df


def main() -> None:
    matches_df, players_df = load_raw_tables()

    stadium_rates = aggregate_stadium_rates(matches_df)
    map_df = filter_stadiums_for_map(stadium_rates)
    print(f"Stadiums with enough matches: {len(map_df)}")

    map_df = geocode_stadiums(map_df)
    stadium_cols = [c for c in STADIUM_EXPORT_COLUMNS if c in map_df.columns]
    stadium_export = map_df[stadium_cols]
    STADIUM_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    stadium_export.to_csv(STADIUM_CSV_PATH, index=False)
    print(f"Wrote {STADIUM_CSV_PATH} ({len(stadium_export)} stadiums)")

    coach_rates = aggregate_coach_rates(matches_df, players_df)
    coach_cols = [c for c in COACH_EXPORT_COLUMNS if c in coach_rates.columns]
    coach_export = coach_rates[coach_cols]
    coach_export.to_csv(COACH_CSV_PATH, index=False)
    print(f"Wrote {COACH_CSV_PATH} ({len(coach_export)} coaches)")


if __name__ == "__main__":
    main()
