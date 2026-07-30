"""App-side paths, view-mode registry, and Plotly defaults."""

from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
CSV_PATH = APP_DIR / "stadium_win_rates.csv"
COACH_CSV_PATH = APP_DIR / "coach_win_rates.csv"

RATE_OPTIONS = {
    "home": {
        "column": "home_win_rate",
        "title": "Home Team Win Rate by Stadium",
        "colorbar": "Home win rate (%)",
        "rate_header": "Home win rate (%)",
        "table_title": "Highest home win rates",
        "applies_to_coach": True,
    },
    "away": {
        "column": "away_win_rate",
        "title": "Away Team Win Rate by Stadium",
        "colorbar": "Away win rate (%)",
        "rate_header": "Away win rate (%)",
        "table_title": "Highest away win rates",
        "applies_to_coach": True,
    },
    "draw": {
        "column": "draw_rate",
        "title": "Draw Rate by Stadium",
        "colorbar": "Draw rate (%)",
        "rate_header": "Draw rate (%)",
        "table_title": "Highest draw rates",
        "applies_to_coach": False,
    },
}

COLOR_SCALE = "RdYlGn"
RANGE_COLOR = [0, 100]
PROJECTION = "natural earth"
SIZE_MAX = 28

DEFAULT_MIN_MATCHES = 3
YEAR_MIN = 1930
YEAR_MAX = 2014
