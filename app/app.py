"""Stadium home/away win-rate world map Dash app."""

from dash import Dash
from flask_caching import Cache

import data as data_module
from layout import build_layout

app = Dash(__name__)
server = app.server

cache = Cache(
    app.server,
    config={"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 3600},
)
data_module.init_cache(cache)

app.layout = build_layout()

# Register callbacks (side-effect import after cache is wired)
import callbacks  # noqa: E402, F401

if __name__ == "__main__":
    app.run(debug=True)
