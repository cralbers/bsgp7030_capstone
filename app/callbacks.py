"""Dash callbacks wiring the Home/Away radio to figures and grids."""

from __future__ import annotations

from dash import Input, Output, callback

from config import RATE_OPTIONS
from figures import build_coach_scatter, build_win_rate_map
from tables import (
    build_coach_column_defs,
    build_coach_rows,
    build_top_stadiums_column_defs,
    build_top_stadiums_rows,
)


@callback(
    Output("stadium-win-rate-map", "figure"),
    Output("top-stadiums-grid", "rowData"),
    Output("top-stadiums-grid", "columnDefs"),
    Output("top-stadiums-title", "children"),
    Input("win-rate-mode-radio", "value"),
)
def update_map_and_table(rate_mode: str):
    mode = rate_mode or "home"
    meta = RATE_OPTIONS.get(mode, RATE_OPTIONS["home"])
    return (
        build_win_rate_map(mode),
        build_top_stadiums_rows(mode),
        build_top_stadiums_column_defs(mode),
        meta["table_title"],
    )


@callback(
    Output("coach-home-away-scatter", "figure"),
    Output("top-coaches-grid", "rowData"),
    Output("top-coaches-grid", "columnDefs"),
    Output("top-coaches-title", "children"),
    Input("win-rate-mode-radio", "value"),
)
def update_coach_scatter(rate_mode: str):
    mode = rate_mode or "home"
    return (
        build_coach_scatter(mode),
        build_coach_rows(),
        build_coach_column_defs(),
        "Coach win rates",
    )
