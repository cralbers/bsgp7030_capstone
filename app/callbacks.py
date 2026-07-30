"""Dash callbacks wiring filters to figures and grids."""

from __future__ import annotations

from dash import Input, Output, callback

from config import DEFAULT_MIN_MATCHES, RATE_OPTIONS, YEAR_MAX, YEAR_MIN
from figures import build_coach_scatter, build_win_rate_map
from tables import (
    build_coach_column_defs,
    build_coach_rows,
    build_top_stadiums_column_defs,
    build_top_stadiums_rows,
)


def _parse_filters(rate_mode, min_matches, year_range):
    mode = rate_mode or "home"
    matches = int(min_matches) if min_matches is not None else DEFAULT_MIN_MATCHES
    if year_range and len(year_range) == 2:
        year_start, year_end = int(year_range[0]), int(year_range[1])
    else:
        year_start, year_end = YEAR_MIN, YEAR_MAX
    return mode, matches, year_start, year_end


@callback(
    Output("stadium-win-rate-map", "figure"),
    Output("top-stadiums-grid", "rowData"),
    Output("top-stadiums-grid", "columnDefs"),
    Output("top-stadiums-title", "children"),
    Input("win-rate-mode-radio", "value"),
    Input("min-matches-slider", "value"),
    Input("year-range-slider", "value"),
)
def update_map_and_table(rate_mode, min_matches, year_range):
    mode, matches, year_start, year_end = _parse_filters(
        rate_mode, min_matches, year_range
    )
    meta = RATE_OPTIONS.get(mode, RATE_OPTIONS["home"])
    return (
        build_win_rate_map(
            mode,
            min_matches=matches,
            year_start=year_start,
            year_end=year_end,
        ),
        build_top_stadiums_rows(
            mode,
            min_matches=matches,
            year_start=year_start,
            year_end=year_end,
        ),
        build_top_stadiums_column_defs(mode),
        meta["table_title"],
    )


@callback(
    Output("coach-home-away-scatter", "figure"),
    Output("top-coaches-grid", "rowData"),
    Output("top-coaches-grid", "columnDefs"),
    Output("top-coaches-title", "children"),
    Input("win-rate-mode-radio", "value"),
    Input("min-matches-slider", "value"),
    Input("year-range-slider", "value"),
)
def update_coach_scatter(rate_mode, min_matches, year_range):
    mode, matches, year_start, year_end = _parse_filters(
        rate_mode, min_matches, year_range
    )
    return (
        build_coach_scatter(
            mode,
            min_matches=matches,
            year_start=year_start,
            year_end=year_end,
        ),
        build_coach_rows(
            min_matches=matches,
            year_start=year_start,
            year_end=year_end,
        ),
        build_coach_column_defs(),
        "Coach win rates",
    )
