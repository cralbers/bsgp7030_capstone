"""Static Dash layout for the win-rate dashboard."""

from __future__ import annotations

import dash_ag_grid as dag
from dash import dcc, html

from config import DEFAULT_MIN_MATCHES, YEAR_MAX, YEAR_MIN


def build_layout():
    """Return the full page layout."""
    return html.Div(
        className="app-container",
        children=[
            html.Header(
                className="app-header",
                children=[
                    html.H1("World Cup Stadium Win Rates", className="app-title"),
                    html.P(
                        "Compare home, away, and draw rates at FIFA World Cup stadiums. "
                        "The year filter keeps stadiums/coaches active in that span; "
                        "rates still use all of their World Cup matches.",
                        className="app-subtitle",
                    ),
                ],
            ),
            html.Div(
                className="map-controls",
                children=[
                    html.Div(
                        className="map-controls-field",
                        children=[
                            html.Span("Show rate:", className="map-controls-label"),
                            dcc.RadioItems(
                                id="win-rate-mode-radio",
                                className="win-rate-radio",
                                options=[
                                    {"label": "Home", "value": "home"},
                                    {"label": "Away", "value": "away"},
                                    {"label": "Draw", "value": "draw"},
                                ],
                                value="home",
                                inline=True,
                            ),
                        ],
                    ),
                    html.Div(
                        className="map-controls-field",
                        children=[
                            html.Span(
                                "Min matches:",
                                className="map-controls-label",
                            ),
                            dcc.Slider(
                                id="min-matches-slider",
                                min=1,
                                max=10,
                                step=1,
                                value=DEFAULT_MIN_MATCHES,
                                marks={i: str(i) for i in range(1, 11)},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": False,
                                },
                            ),
                        ],
                    ),
                    html.Div(
                        className="map-controls-field",
                        style={"minWidth": "260px", "flex": "1"},
                        children=[
                            html.Span("Years:", className="map-controls-label"),
                            dcc.RangeSlider(
                                id="year-range-slider",
                                min=YEAR_MIN,
                                max=YEAR_MAX,
                                step=4,
                                value=[YEAR_MIN, YEAR_MAX],
                                marks={
                                    y: str(y)
                                    for y in range(YEAR_MIN, YEAR_MAX + 1, 20)
                                },
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": False,
                                },
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="map-panel",
                children=[
                    dcc.Loading(
                        id="stadium-win-rate-loading",
                        type="circle",
                        children=dcc.Graph(
                            id="stadium-win-rate-map",
                            figure={},
                            config={"displayModeBar": True, "responsive": True},
                        ),
                    ),
                ],
            ),
            html.Div(
                className="table-panel",
                children=[
                    html.H2(id="top-stadiums-title", className="table-title"),
                    dag.AgGrid(
                        id="top-stadiums-grid",
                        rowData=[],
                        columnDefs=[],
                        columnSize="responsiveSizeToFit",
                        defaultColDef={"filter": True, "sortable": True},
                        dashGridOptions={
                            "theme": "themeBalham",
                            "animateRows": True,
                            "pagination": True,
                            "paginationPageSize": 10,
                        },
                    ),
                ],
            ),
            html.Div(
                className="coach-panel",
                children=[
                    html.H2(
                        "Coach home vs away win rates",
                        className="table-title",
                    ),
                    html.P(
                        "Each point is a coach meeting the min-matches filter for both "
                        "home and away roles. The dashed line is equal home and away "
                        "win rates. Draw mode colors the stadium map only.",
                        className="app-subtitle",
                    ),
                    dcc.Loading(
                        id="coach-scatter-loading",
                        type="circle",
                        children=dcc.Graph(
                            id="coach-home-away-scatter",
                            figure={},
                            config={"displayModeBar": True, "responsive": True},
                        ),
                    ),
                ],
            ),
            html.Div(
                className="table-panel",
                children=[
                    html.H2(id="top-coaches-title", className="table-title"),
                    dag.AgGrid(
                        id="top-coaches-grid",
                        rowData=[],
                        columnDefs=[],
                        columnSize="responsiveSizeToFit",
                        defaultColDef={"filter": True, "sortable": True},
                        dashGridOptions={
                            "theme": "themeBalham",
                            "animateRows": True,
                            "pagination": True,
                            "paginationPageSize": 10,
                        },
                    ),
                ],
            ),
        ],
    )
