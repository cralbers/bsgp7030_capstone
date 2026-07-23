"""Plotly figure builders for stadium map and coach scatter."""

from __future__ import annotations

import plotly.express as px

from config import (
    COLOR_SCALE,
    PROJECTION,
    RANGE_COLOR,
    RATE_OPTIONS,
    SIZE_MAX,
)
from data import load_coach_win_rates, load_stadium_win_rates
from theme import COLORS


def build_win_rate_map(rate_mode: str):
    """Build a scatter_geo figure colored by home or away win rate."""
    df = load_stadium_win_rates()
    meta = RATE_OPTIONS.get(rate_mode, RATE_OPTIONS["home"])
    rate_col = meta["column"]
    hover_cols = ["Stadium", "City", "matches"]

    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        color=rate_col,
        size="matches",
        hover_name="Stadium",
        hover_data={c: True for c in hover_cols}
        | {rate_col: ":.1f", "lat": False, "lon": False},
        color_continuous_scale=COLOR_SCALE,
        range_color=RANGE_COLOR,
        projection=PROJECTION,
        title=meta["title"],
        size_max=SIZE_MAX,
    )
    fig.update_layout(
        coloraxis_colorbar_title=meta["colorbar"],
        height=500,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor=COLORS["surface"],
        font_color=COLORS["text"],
    )
    return fig


def build_coach_scatter(rate_mode: str):
    """Scatter of coach home (x) vs away (y), colored by selected win rate."""
    df = load_coach_win_rates()
    meta = RATE_OPTIONS.get(rate_mode, RATE_OPTIONS["home"])
    rate_col = meta["column"]
    fig = px.scatter(
        df,
        x="home_win_rate",
        y="away_win_rate",
        color=rate_col,
        size="total_matches",
        hover_name="Coach Name",
        hover_data={
            "home_matches": True,
            "away_matches": True,
            "home_win_rate": ":.1f",
            "away_win_rate": ":.1f",
            "total_matches": True,
        },
        color_continuous_scale=COLOR_SCALE,
        range_color=RANGE_COLOR,
        title="Coach Win Rates: Home vs Away",
        labels={
            "home_win_rate": "Home win rate (%)",
            "away_win_rate": "Away win rate (%)",
            "total_matches": "Total matches",
        },
        size_max=SIZE_MAX,
    )
    fig.add_shape(
        type="line",
        x0=0,
        y0=0,
        x1=100,
        y1=100,
        line=dict(color="gray", dash="dash", width=1),
    )
    fig.update_xaxes(range=[0, 100])
    fig.update_yaxes(range=[0, 100])
    fig.update_layout(
        coloraxis_colorbar_title=meta["colorbar"],
        height=550,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor=COLORS["surface"],
        font_color=COLORS["text"],
    )
    return fig
