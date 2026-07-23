# FIFA World Cup Capstone

Exploratory analysis and a Dash app for FIFA World Cup home vs away win rates by stadium and coach, using the [Kaggle FIFA World Cup dataset](https://www.kaggle.com/datasets/abecklas/fifa-world-cup/data).

## Main directory


| File / folder    | Description                                                                                                          |
| ---------------- | -------------------------------------------------------------------------------------------------------------------- |
| `eda.ipynb`      | Exploratory analysis: load cups, matches, and players; inspect schemas; early goal-trend plots.                      |
| `analysis.ipynb` | Stadium home/away win rates, geocoding, world maps; coach home/away rates and scatter (exploratory).                  |
| `src/fifa_wc/`   | Shared ETL helpers: match outcomes, stadium/coach aggregation, geocoding with disk cache.                            |
| `scripts/`       | `build_app_csvs.py` regenerates the app CSVs from local `data/` or Kaggle.                                           |
| `env.yml`        | Conda environment export (channels and package dependencies) used for notebooks and the Dash app.                    |
| `run_app.sh`     | Activates the `capstone` conda environment and launches the Dash app.                                                |
| `.gitignore`     | Paths excluded from version control.                                                                                 |
| `app/`           | Dash web application (see below).                                                                                    |




## `app/` folder


| File                        | Description                                                                                                                                                                 |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app/app.py`                | Dash entrypoint: creates the app, cache, layout, and registers callbacks.                                                                                                   |
| `app/config.py`             | CSV paths, Home/Away `RATE_OPTIONS`, and Plotly defaults.                                                                                                                   |
| `app/schema.py`             | Required CSV columns and validation on load.                                                                                                                                |
| `app/data.py`               | Cached CSV loaders (after schema validation).                                                                                                                               |
| `app/figures.py`            | Stadium map and coach scatter builders.                                                                                                                                     |
| `app/tables.py`             | AgGrid row/column builders for stadium and coach tables.                                                                                                                    |
| `app/layout.py`             | Static page layout.                                                                                                                                                         |
| `app/callbacks.py`          | Home/Away radio → map, tables, and scatter.                                                                                                                                 |
| `app/theme.py`              | Shared color, spacing, and font constants.                                                                                                                                  |
| `app/assets/style.css`      | Layout and panel styles for the app.                                                                                                                                        |
| `app/stadium_win_rates.csv` | Precomputed stadium win rates with latitude/longitude (committed so the app runs without rebuilding).                                                                       |
| `app/coach_win_rates.csv`   | Precomputed coach home/away win rates (committed so the app runs without rebuilding).                                                                                       |
| `app/requirements.txt`      | Python package dependencies for the Dash app.                                                                                                                               |




## How to run the app

Create or update the conda environment from the project export if needed:

```bash
conda env create -f env.yml
# or: conda env update -f env.yml --prune
```

Then:

```bash
# from the repository root
./run_app.sh
```

Or manually:

```bash
conda activate capstone
cd app
python app.py
```

Install app dependencies if needed: `pip install -r app/requirements.txt`.

## Regenerating app CSVs

Committed CSVs under `app/` are enough to run the dashboard. To rebuild them from raw data (local `data/WorldCupMatches.csv` and `data/WorldCupPlayers.csv`, or Kaggle if those are missing):

```bash
conda activate capstone
# from the repository root
python scripts/build_app_csvs.py
```

Geocoding uses `data/geocode_cache.json` (and seeds from the existing stadium CSV) so repeat runs stay fast.
