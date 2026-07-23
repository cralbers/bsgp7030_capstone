"""Static Dash layout for the win-rate dashboard."""

from __future__ import annotations

import dash_ag_grid as dag
from dash import dcc, html


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
                        "Compare home and away team win rates at FIFA World Cup stadiums "
                        "(stadiums with at least 3 matches).",
                        className="app-subtitle",
                    ),
                ],
            ),
            html.Div(
                className="map-controls",
                children=[
                    html.Span("Show win rate for:", className="map-controls-label"),
                    dcc.RadioItems(
                        id="win-rate-mode-radio",
                        className="win-rate-radio",
                        options=[
                            {"label": "Home", "value": "home"},
                            {"label": "Away", "value": "away"},
                        ],
                        value="home",
                        inline=True,
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
                        "Each point is a coach with at least 3 home and 3 away World Cup matches. "
                        "The dashed line is equal home and away win rates.",
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
