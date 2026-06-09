#!/usr/bin/env python3
"""
Stage 1: Import/Clean - Simplified
"""
import sqlite3
import gzip
import re
import sys
from pathlib import Path
import zipfile

import os
BASE_DIR = os.environ.get("KEMV_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "data", "kemv.db")
POP_PATH = os.path.join(BASE_DIR, "data", "estat_tgs00096.tsv.gz")
FUA_DIR = os.path.join(BASE_DIR, "data", "Results", "2021")
RASTER_PATH = os.path.join(BASE_DIR, "data", "Results", "TCD_2015_020m_eu_03035_d05_Full", "TCD_2015_020m_eu_03035_d05_full.tif")
NUTS_XLSX = os.path.join(BASE_DIR, "data", "NUTS2021.xlsx")

PIXEL_KM2 = 400 / 1_000_000

print("Stage 1: Import/Clean", flush=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS regions")
c.execute("""CREATE TABLE regions (
    id INTEGER PRIMARY KEY, name TEXT, nuts_code TEXT, population INTEGER, 
    area_km2 REAL, tree_cover_km2 REAL, tree_cover_pct REAL
)""")
conn.commit()

print("1. Reading population...", flush=True)
pop_data = {}
with gzip.open(POP_PATH, 'rt') as f:
    for line in f:
        parts = line.strip().split('\t')
        geo = parts[0].split(',')[-1]
        if re.match(r'^[A-Z]{2}[0-9]{2,3}$', geo):
            for val in reversed(parts[1:]):
                val = val.strip()
                if val and val != ':' and not val.endswith('b'):
                    try:
                        pop_data[geo] = int(val.replace(' ', ''))
                        break
                    except:
                        continue

print(f"   Pop regions: {len(pop_data)}", flush=True)

print("2. Reading NUTS mapping...", flush=True)
import pandas as pd
df = pd.read_excel(NUTS_XLSX, sheet_name='Metropolitan')
metro = df[df['METRO (No/Yes)'] == 'Y']
nuts_map = {}
for _, row in metro.iterrows():
    nuts = str(row['NUTS ID'])[:4]
    label = row['METRO LABEL']
    if pd.notna(label) and nuts not in nuts_map:
        nuts_map[nuts] = label

print(f"   NUTS2 mappings: {len(nuts_map)}", flush=True)

def norm(name):
    if not name: return ""
    name = str(name).lower()
    for old, new in [('wien','vienna'),('praha','prague'),('lefkosia','nicosia'),('bruxelles','brussels')]:
        name = name.replace(old, new)
    return name.strip()

merged = {}
for nuts, pop in pop_data.items():
    name = nuts
    nuts2 = nuts[:4]
    if nuts2 in nuts_map:
        name = nuts_map[nuts2]
    key = norm(name)
    if key not in merged or merged[key][2] < pop:
        merged[key] = (nuts, name, pop)

print(f"   Merged: {len(merged)}", flush=True)

print("3. Processing FUA tree cover...", flush=True)
zip_files = list(Path(FUA_DIR).glob("*.zip"))
fua_map = {}
for zf in zip_files:
    m = re.search(r'V025ha_([A-Z]{2}[0-9]{3}L[0-9])_(.+?)_', zf.stem)
    if m:
        fua_map[norm(m.group(2))] = m.group(1)

matched = set(merged.keys()) & set(fua_map.keys())
print(f"   Matched: {len(matched)}", flush=True)

processed = 0
results = {}

for i, key in enumerate(sorted(matched)):
    if i % 5 == 0:
        print(f"   {i}/{len(matched)}", flush=True)
        sys.stdout.flush()
    
    _, name, pop = merged[key]
    fua_code = fua_map[key]
    
    zf_path = None
    for zf in zip_files:
        if fua_code in zf.stem:
            zf_path = str(zf)
            break
    
    if not zf_path:
        continue
    
    try:
        import tempfile
        import rasterio
        import numpy as np
        from shapely.geometry import shape
        from shapely.ops import unary_union
        import fiona
    except ImportError as e:
        print(f"   Import error: {e}", flush=True)
        break
    
    try:
        with tempfile.TemporaryDirectory() as tmpd:
            with zipfile.ZipFile(zf_path, 'r') as z:
                z.extractall(tmpd)
            
            fgb = list(Path(tmpd).glob("**/*.fgb"))
            if not fgb:
                continue
            
            geoms = []
            with fiona.open(fgb[0], 'r') as src:
                for f in src:
                    g = shape(f['geometry'])
                    if g.is_valid:
                        geoms.append(g)
                    if len(geoms) >= 500:
                        break
            
            if not geoms:
                continue
            
            union = unary_union(geoms)
            area_km2 = union.area / 1_000_000
            
            with rasterio.open(RASTER_PATH) as rst:
                bbox = union.bounds
                window = rasterio.windows.from_bounds(
                    int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]),
                    rst.transform
                )
                # Round window to integers to avoid shape mismatch
                col_off = int(round(window.col_off))
                row_off = int(round(window.row_off))
                width = int(round(window.width))
                height = int(round(window.height))
                window = rasterio.windows.Window(col_off, row_off, width, height)
                
                data = rst.read(window=window)
                
                from rasterio.features import geometry_mask
                mask = geometry_mask([union], out_shape=(height, width), 
                                transform=rst.window_transform(window), invert=True)
                
                tree_pix = int(np.sum((data[0] > 0) & mask))
                tree_km2 = tree_pix * PIXEL_KM2
                tree_pct = (tree_km2 / area_km2 * 100) if area_km2 > 0 else 0
            
            results[key] = (fua_code, area_km2, tree_km2, tree_pct)
            processed += 1
            
    except Exception as e:
        continue

print(f"   Processed: {processed}", flush=True)

print("4. Saving to DB...", flush=True)
sorted_regions = sorted(merged.values(), key=lambda x: x[2], reverse=True)
for nuts, name, pop in sorted_regions:
    key = norm(name)
    info = results.get(key, (None, None, None, None))
    c.execute("INSERT INTO regions (name, nuts_code, population, area_km2, tree_cover_km2, tree_cover_pct) VALUES (?, ?, ?, ?, ?, ?)",
             (name, nuts, pop, info[1], info[2], info[3]))

conn.commit()

c.execute("SELECT COUNT(*) FROM regions")
total = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM regions WHERE tree_cover_km2 IS NOT NULL")
with_tree = c.fetchone()[0]

print(f"Done! {total} regions ({with_tree} with tree data)", flush=True)

conn.close()