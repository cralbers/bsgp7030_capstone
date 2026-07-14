"""Stadium home/away win-rate world map Dash app."""

from pathlib import Path

import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html
from flask_caching import Cache

from theme import COLORS

CSV_PATH = Path(__file__).resolve().parent / "stadium_win_rates.csv"

app = Dash(__name__)
server = app.server

cache = Cache(
    app.server,
    config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 3600},
)

RATE_OPTIONS = {
    "home": {
        "column": "home_win_rate",
        "title": "Home Team Win Rate by Stadium",
        "colorbar": "Home win rate (%)",
        "rate_header": "Home win rate (%)",
        "table_title": "Highest home win rates",
    },
    "away": {
        "column": "away_win_rate",
        "title": "Away Team Win Rate by Stadium",
        "colorbar": "Away win rate (%)",
        "rate_header": "Away win rate (%)",
        "table_title": "Highest away win rates",
    },
}


@cache.memoize()
def load_stadium_win_rates() -> pd.DataFrame:
    """Load precomputed stadium win rates and coordinates."""
    return pd.read_csv(CSV_PATH)


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
        color_continuous_scale="RdYlGn",
        range_color=[0, 100],
        projection="natural earth",
        title=meta["title"],
        size_max=28,
    )
    fig.update_layout(
        coloraxis_colorbar_title=meta["colorbar"],
        height=500,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor=COLORS["surface"],
        font_color=COLORS["text"],
    )
    return fig


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


app.layout = html.Div(
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
    ],
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


if __name__ == "__main__":
    app.run(debug=True)
