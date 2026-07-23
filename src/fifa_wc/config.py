"""ETL thresholds and default paths."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
APP_DIR = REPO_ROOT / "app"

MIN_STADIUM_MATCHES = 3
MIN_COACH_HOME = 3
MIN_COACH_AWAY = 3

MATCHES_CSV = DATA_DIR / "WorldCupMatches.csv"
PLAYERS_CSV = DATA_DIR / "WorldCupPlayers.csv"
GEOCODE_CACHE_PATH = DATA_DIR / "geocode_cache.json"
STADIUM_CSV_PATH = APP_DIR / "stadium_win_rates.csv"
COACH_CSV_PATH = APP_DIR / "coach_win_rates.csv"

KAGGLE_DATASET = "abecklas/fifa-world-cup"
