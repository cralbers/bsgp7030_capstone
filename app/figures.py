"""Plotly figure builders for stadium map and coach scatter."""

from __future__ import annotations

import plotly.express as px

from config import (
    COLOR_SCALE,
    DEFAULT_MIN_MATCHES,
    PROJECTION,
    RANGE_COLOR,
    RATE_OPTIONS,
    SIZE_MAX,
    YEAR_MAX,
    YEAR_MIN,
)
from data import filter_coaches, filter_stadiums
from theme import COLORS


def build_win_rate_map(
    rate_mode: str,
    *,
    min_matches: int = DEFAULT_MIN_MATCHES,
    year_start: int = YEAR_MIN,
    year_end: int = YEAR_MAX,
):
    """Build a scatter_geo figure colored by selected rate mode."""
    df = filter_stadiums(
        min_matches=min_matches,
        year_start=year_start,
        year_end=year_end,
    )
    meta = RATE_OPTIONS.get(rate_mode, RATE_OPTIONS["home"])
    rate_col = meta["column"]
    if rate_col not in df.columns:
        rate_col = "home_win_rate"
        meta = RATE_OPTIONS["home"]
    hover_cols = ["Stadium", "City", "matches"]

    if df.empty:
        fig = px.scatter_geo(title=meta["title"])
        fig.update_layout(
            height=500,
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor=COLORS["surface"],
            font_color=COLORS["text"],
            annotations=[
                dict(
                    text="No stadiums match the current filters",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                )
            ],
        )
        return fig

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


def build_coach_scatter(
    rate_mode: str,
    *,
    min_matches: int = DEFAULT_MIN_MATCHES,
    year_start: int = YEAR_MIN,
    year_end: int = YEAR_MAX,
):
    """Scatter of coach home (x) vs away (y), colored by selected win rate."""
    df = filter_coaches(
        min_matches=min_matches,
        year_start=year_start,
        year_end=year_end,
    )
    meta = RATE_OPTIONS.get(rate_mode, RATE_OPTIONS["home"])
    use_rate_color = meta.get("applies_to_coach", True)
    rate_col = meta["column"] if use_rate_color else None

    if df.empty:
        fig = px.scatter(title="Coach Win Rates: Home vs Away")
        fig.update_layout(
            height=550,
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor=COLORS["surface"],
            font_color=COLORS["text"],
            annotations=[
                dict(
                    text="No coaches match the current filters",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                )
            ],
        )
        return fig

    scatter_kwargs = dict(
        data_frame=df,
        x="home_win_rate",
        y="away_win_rate",
        size="total_matches",
        hover_name="Coach Name",
        hover_data={
            "home_matches": True,
            "away_matches": True,
            "home_win_rate": ":.1f",
            "away_win_rate": ":.1f",
            "total_matches": True,
        },
        title="Coach Win Rates: Home vs Away",
        labels={
            "home_win_rate": "Home win rate (%)",
            "away_win_rate": "Away win rate (%)",
            "total_matches": "Total matches",
        },
        size_max=SIZE_MAX,
    )
    if rate_col and rate_col in df.columns:
        scatter_kwargs["color"] = rate_col
        scatter_kwargs["color_continuous_scale"] = COLOR_SCALE
        scatter_kwargs["range_color"] = RANGE_COLOR

    fig = px.scatter(**scatter_kwargs)
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
    layout_kwargs = dict(
        height=550,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor=COLORS["surface"],
        font_color=COLORS["text"],
    )
    if rate_col and rate_col in df.columns:
        layout_kwargs["coloraxis_colorbar_title"] = meta["colorbar"]
    fig.update_layout(**layout_kwargs)
    return fig
