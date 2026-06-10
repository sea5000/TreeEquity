#!/usr/bin/env python3
"""Import city_tree_rankings.csv into kemv.db with optional geocoding."""

import csv
import json
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE / "capstone_1" / "data" / "kemv.db"
CSV_PATH = BASE / "capstone_1" / "data" / "city_tree_rankings.csv"


def geocode(city, country):
    try:
        q = urllib.parse.quote(f"{city}, {country}")
        url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "KEMV-Dashboard/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None, None


def main():
    do_geocode = "--geocode" in sys.argv

    with open(CSV_PATH) as f:
        rows = list(csv.DictReader(f))

    print(f"Read {len(rows)} cities from CSV")

    # Fix data errors
    for row in rows:
        if row["city"].strip().lower() == "vilnius" and row["country"].strip().lower() == "liechtenstein":
            print('  Fixed: Vilnius, Liechtenstein → Vilnius, Lithuania')
            row["country"] = "Lithuania"

    # Sort by pop_to_tree_ratio ascending (1 = best equity)
    for row in rows:
        row["_ratio"] = float(row["pop_to_tree_ratio"])
    rows.sort(key=lambda r: r["_ratio"])
    for i, row in enumerate(rows, 1):
        row["_rank"] = i

    # Grab existing coords from cities table
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    existing = {}
    try:
        cur.execute("SELECT LOWER(TRIM(name)), lat, lon FROM cities WHERE lat IS NOT NULL")
        for name, lat, lon in cur.fetchall():
            existing[name] = (lat, lon)
    except Exception:
        pass

    cities = []
    for row in rows:
        key = row["city"].strip().lower()
        coords = existing.get(key, (None, None))
        cities.append({
            "city": row["city"].strip(),
            "country": row["country"].strip(),
            "population": int(float(row["population"])) if row["population"] else 0,
            "urban_area_km2": float(row["urban_area_km2"]) if row["urban_area_km2"] else 0,
            "tree_cover_km2": float(row["tree_cover_km2"]) if row["tree_cover_km2"] else 0,
            "tree_percentage": float(row["tree_percentage"]) if row["tree_percentage"] else 0,
            "population_density": float(row["population_density"]) if row["population_density"] else 0,
            "tree_density_per_km2": float(row["tree_density_per_km2"]) if row["tree_density_per_km2"] else 0,
            "pop_to_tree_ratio": float(row["pop_to_tree_ratio"]) if row["pop_to_tree_ratio"] else 0,
            "rank": row["_rank"],
            "lat": coords[0],
            "lon": coords[1],
        })

    # Geocode cities without coordinates
    if do_geocode:
        need = [c for c in cities if c["lat"] is None]
        print(f"Geocoding {len(need)} cities via Nominatim...")
        for i, c in enumerate(need):
            print(f"  [{i+1}/{len(need)}] {c['city']}, {c['country']}...", end=" ", flush=True)
            lat, lon = geocode(c["city"], c["country"])
            if lat is not None:
                c["lat"] = lat
                c["lon"] = lon
                print(f"\u2713 ({lat:.4f}, {lon:.4f})")
            else:
                print("\u2717 not found")
            if i < len(need) - 1:
                time.sleep(1)

    # Create table and insert
    print("Creating city_tree_rankings table...")
    cur.execute("DROP TABLE IF EXISTS city_tree_rankings")
    cur.execute("""
        CREATE TABLE city_tree_rankings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            population INTEGER,
            urban_area_km2 REAL,
            tree_cover_km2 REAL,
            tree_percentage REAL,
            population_density REAL,
            tree_density_per_km2 REAL,
            pop_to_tree_ratio REAL,
            rank INTEGER,
            lat REAL,
            lon REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    for c in cities:
        cur.execute("""
            INSERT INTO city_tree_rankings
            (city, country, population, urban_area_km2, tree_cover_km2, tree_percentage,
             population_density, tree_density_per_km2, pop_to_tree_ratio, rank, lat, lon)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (c["city"], c["country"], c["population"], c["urban_area_km2"],
              c["tree_cover_km2"], c["tree_percentage"], c["population_density"],
              c["tree_density_per_km2"], c["pop_to_tree_ratio"], c["rank"],
              c["lat"], c["lon"]))

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM city_tree_rankings")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM city_tree_rankings WHERE lat IS NOT NULL")
    with_coords = cur.fetchone()[0]
    conn.close()

    print(f"Done! {total} cities inserted ({with_coords} with coordinates)")


if __name__ == "__main__":
    main()
