# FIFA World Cup Capstone

Exploratory analysis and a Dash app for FIFA World Cup home vs away win rates by stadium and coach, using the [Kaggle FIFA World Cup dataset](https://www.kaggle.com/datasets/abecklas/fifa-world-cup/data).

## Main directory


| File / folder    | Description                                                                                                          |
| ---------------- | -------------------------------------------------------------------------------------------------------------------- |
| `eda.ipynb`      | Exploratory analysis: load cups, matches, and players; inspect schemas; early goal-trend plots.                      |
| `analysis.ipynb` | Stadium home/away win rates, geocoding, world maps; coach home/away rates and scatter; exports CSVs used by the app. |
| `env.yml`        | Conda environment export (channels and package dependencies) used for notebooks and the Dash app.                    |
| `run_app.sh`     | Activates the `capstone` conda environment and launches the Dash app.                                                |
| `.gitignore`     | Paths excluded from version control.                                                                                 |
| `app/`           | Dash web application (see below).                                                                                    |




## `app/` folder


| File                        | Description                                                                                                                                                                 |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app/app.py`                | Dash app: stadium world map, top-stadiums table, coach home-vs-away scatter, coaches table. A Home/Away radio controls map color, stadium sorting, and coach scatter color. |
| `app/theme.py`              | Shared color, spacing, and font constants.                                                                                                                                  |
| `app/assets/style.css`      | Layout and panel styles for the app.                                                                                                                                        |
| `app/stadium_win_rates.csv` | Precomputed stadium win rates with latitude/longitude (from `analysis.ipynb`).                                                                                              |
| `app/coach_win_rates.csv`   | Precomputed coach home/away win rates (from `analysis.ipynb`).                                                                                                              |
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