"""Clean match rows and attach home/away/draw outcome flags."""

from __future__ import annotations

import pandas as pd


def clean_matches_for_stadiums(matches_df: pd.DataFrame) -> pd.DataFrame:
    """Strip stadium/city, coerce goals, drop bad rows, add outcome flags."""
    m = matches_df.copy()
    m["Stadium"] = m["Stadium"].astype(str).str.strip()
    m["City"] = m["City"].astype(str).str.strip()
    m["Home Team Goals"] = pd.to_numeric(m["Home Team Goals"], errors="coerce")
    m["Away Team Goals"] = pd.to_numeric(m["Away Team Goals"], errors="coerce")
    if "Year" in m.columns:
        m["Year"] = pd.to_numeric(m["Year"], errors="coerce")
    m = m.dropna(subset=["Stadium", "Home Team Goals", "Away Team Goals"])
    m = m[m["Stadium"].ne("") & m["Stadium"].ne("nan")]

    m["home_win"] = (m["Home Team Goals"] > m["Away Team Goals"]).astype(int)
    m["away_win"] = (m["Home Team Goals"] < m["Away Team Goals"]).astype(int)
    m["draw"] = (m["Home Team Goals"] == m["Away Team Goals"]).astype(int)
    return m


def clean_matches_for_coaches(matches_df: pd.DataFrame) -> pd.DataFrame:
    """Coerce goals and drop rows missing match/team identifiers."""
    m = matches_df.copy()
    m["Home Team Goals"] = pd.to_numeric(m["Home Team Goals"], errors="coerce")
    m["Away Team Goals"] = pd.to_numeric(m["Away Team Goals"], errors="coerce")
    if "Year" in m.columns:
        m["Year"] = pd.to_numeric(m["Year"], errors="coerce")
    return m.dropna(
        subset=[
            "MatchID",
            "Home Team Initials",
            "Away Team Initials",
            "Home Team Goals",
            "Away Team Goals",
        ]
    )
