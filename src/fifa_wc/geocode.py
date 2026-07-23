"""Nominatim geocoding with a disk-backed JSON cache."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from fifa_wc.config import GEOCODE_CACHE_PATH, STADIUM_CSV_PATH


def _cache_key(stadium: str, city: str) -> str:
    return f"{stadium.strip()}|{city.strip()}"


def load_geocode_cache(path: Path = GEOCODE_CACHE_PATH) -> dict[str, list[float | None]]:
    """Load cache mapping 'Stadium|City' -> [lat, lon]."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def save_geocode_cache(
    cache: dict[str, list[float | None]],
    path: Path = GEOCODE_CACHE_PATH,
) -> None:
    """Persist geocode cache to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, sort_keys=True)


def seed_cache_from_stadium_csv(
    cache: dict[str, list[float | None]],
    csv_path: Path = STADIUM_CSV_PATH,
) -> int:
    """Seed cache entries from an existing stadium CSV; return how many added."""
    if not csv_path.exists():
        return 0
    df = pd.read_csv(csv_path)
    added = 0
    for _, row in df.iterrows():
        if pd.isna(row.get("lat")) or pd.isna(row.get("lon")):
            continue
        stadium = str(row["Stadium"])
        city = str(row.get("City", "") or "")
        coords = [float(row["lat"]), float(row["lon"])]
        for key in (_cache_key(stadium, city), _cache_key(stadium, "")):
            if key not in cache:
                cache[key] = coords
                added += 1
    return added


def _attach_coords_from_seed_csv(
    stadium_df: pd.DataFrame,
    seed_csv: Path,
) -> pd.DataFrame:
    """Left-merge lat/lon from an existing stadium CSV on Stadium name."""
    out = stadium_df.copy()
    if "lat" not in out.columns:
        out["lat"] = pd.NA
    if "lon" not in out.columns:
        out["lon"] = pd.NA
    if not seed_csv.exists():
        return out

    existing = pd.read_csv(seed_csv)[["Stadium", "lat", "lon"]].drop_duplicates(
        subset=["Stadium"]
    )
    existing = existing.rename(columns={"lat": "_seed_lat", "lon": "_seed_lon"})
    out = out.merge(existing, on="Stadium", how="left")
    out["lat"] = out["lat"].fillna(out["_seed_lat"])
    out["lon"] = out["lon"].fillna(out["_seed_lon"])
    out = out.drop(columns=["_seed_lat", "_seed_lon"])
    filled = out["lat"].notna().sum()
    print(f"Attached coordinates for {filled} stadiums from {seed_csv.name}")
    return out


def geocode_stadiums(
    stadium_df: pd.DataFrame,
    cache_path: Path = GEOCODE_CACHE_PATH,
    seed_csv: Path | None = STADIUM_CSV_PATH,
    user_agent: str = "fifa_world_cup_stadium_maps",
) -> pd.DataFrame:
    """
    Attach lat/lon to stadium rows.

    Prefer an existing stadium CSV (match on Stadium), then the disk cache, then
    Nominatim for any remaining misses.
    """
    out = stadium_df.copy()
    if seed_csv is not None:
        out = _attach_coords_from_seed_csv(out, seed_csv)

    cache = load_geocode_cache(cache_path)
    if seed_csv is not None:
        seeded = seed_cache_from_stadium_csv(cache, seed_csv)
        if seeded:
            print(f"Seeded geocode cache with {seeded} entries from {seed_csv}")

    missing_mask = out["lat"].isna() | out["lon"].isna()
    if not missing_mask.any():
        save_geocode_cache(cache, cache_path)
        return out.dropna(subset=["lat", "lon"]).reset_index(drop=True)

    from geopy.geocoders import Nominatim
    import time

    geolocator = Nominatim(user_agent=user_agent)
    _last_geocode_at = 0.0

    def lookup(stadium: str, city: str) -> tuple[float | None, float | None]:
        nonlocal _last_geocode_at
        city_s = str(city).strip() if pd.notna(city) else ""
        stadium_s = str(stadium).strip()
        for key in (_cache_key(stadium_s, city_s), _cache_key(stadium_s, "")):
            if key in cache:
                lat, lon = cache[key]
                # Cached nulls mean a previous lookup failed; do not retry every run
                return lat, lon

        queries = [f"{stadium_s}, {city_s}" if city_s else stadium_s]
        if city_s:
            queries.append(city_s)

        coords: tuple[float | None, float | None] = (None, None)
        for q in queries:
            elapsed = time.monotonic() - _last_geocode_at
            if elapsed < 1.1:
                time.sleep(1.1 - elapsed)
            try:
                loc = geolocator.geocode(q, timeout=10)
                _last_geocode_at = time.monotonic()
                if loc is not None:
                    coords = (loc.latitude, loc.longitude)
                    break
            except Exception as exc:
                _last_geocode_at = time.monotonic()
                print(f"Geocode failed for {q!r}: {exc}")
                continue

        cache[_cache_key(stadium_s, city_s)] = [coords[0], coords[1]]
        return coords

    need = out.index[missing_mask]
    print(f"Geocoding {len(need)} stadium(s) via Nominatim / cache")
    for idx in need:
        lat, lon = lookup(out.at[idx, "Stadium"], out.at[idx, "City"])
        out.at[idx, "lat"] = lat
        out.at[idx, "lon"] = lon

    save_geocode_cache(cache, cache_path)

    before = len(out)
    out = out.dropna(subset=["lat", "lon"]).reset_index(drop=True)
    dropped = before - len(out)
    if dropped:
        print(f"Dropped {dropped} stadium(s) that could not be geocoded")
    return out
