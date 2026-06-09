#!/usr/bin/env python3
"""
Stage 2: Analysis
Reads from DB, filters by population threshold, outputs rankings.
"""

import sqlite3

DB_PATH = "data/kemv.db"

MAJOR_CITIES = {
    'vienna', 'berlin', 'paris', 'london', 'madrid', 'rome', 'amsterdam',
    'athens', 'athina', 'stockholm', 'prague', 'budapest', 'dublin', 'helsinki',
    'warsaw', 'lisbon', 'copenhagen', 'brussels', 'bucharest', 'sofia',
    'tallinn', 'riga', 'vilnius', 'luxembourg', 'valletta', 'zagreb',
    'ljubljana', 'bratislava', 'nicosia', 'bern', 'oslo',
    'munich', 'milan', 'barcelona', 'hamburg', 'lyon', 'marseille',
    'frankfurt', 'cologne', 'naples', 'turin', 'palermo', 'valencia',
    'seville', 'bilbao', 'hanover', 'dortmund', 'stuttgart', 'dusseldorf', 
    'bremen', 'hannover', 'leipzig', 'dresden',
    'birmingham', 'manchester', 'glasgow', 'liverpool', 'newcastle',
    'bristol', 'sheffield', 'leeds', 'edinburgh',
    'graz', 'linz', 'salzburg', 'innsbruck',
    'antwerp', 'gent', 'charleroi', 'liege',
    'plovdiv', 'varna', 'burgas',
    'zurich', 'geneva', 'basel', 'lausanne',
    'plzen', 'brno', 'ostrava',
    'porto', 'faro',
}


def main():
    print("=" * 50)
    print("Stage 2: Analysis")
    print("=" * 50)
    
    min_population = 100000
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print(f"\n1. Regions with pop >= {min_population:,}")
    c.execute("SELECT name, population FROM regions WHERE population >= ? ORDER BY population DESC", (min_population,))
    all_regions = c.fetchall()
    print(f"   Found: {len(all_regions)}")
    
    print("\n2. Major cities:")
    major = []
    for name, pop in all_regions:
        n = name.lower()
        if any(city in n or n in city for city in MAJOR_CITIES):
            major.append((name, pop))
    
    print(f"   Major cities: {len(major)}")
    for name, pop in major[:20]:
        print(f"     {name}: {pop:,}")
    
    print("\n3. Tree cover rankings:")
    c.execute("""
        SELECT name, population, area_km2, tree_cover_km2, tree_cover_pct
        FROM regions
        WHERE tree_cover_km2 IS NOT NULL
        ORDER BY tree_cover_km2 DESC
    """)
    results = c.fetchall()
    
    print("-" * 60)
    print(f"{'Rank':<5} {'City':<20} {'Pop':>10} {'Area':>8} {'Tree':>8} {'Tree %':>8}")
    print("-" * 60)
    
    for i, (name, pop, area, tree, pct) in enumerate(results[:30], 1):
        area_str = f"{area:.1f}" if area else "-"
        tree_str = f"{tree:.1f}" if tree else "-"
        pct_str = f"{pct:.1f}%" if pct else "-"
        print(f"{i:<5} {name:<20} {pop:>10,} {area_str:>8} {tree_str:>8} {pct_str:>8}")
    
    conn.close()
    print("\nDone!")


if __name__ == "__main__":
    main()