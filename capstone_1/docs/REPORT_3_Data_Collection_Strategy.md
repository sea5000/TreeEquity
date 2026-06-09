# Report 3: Data Collection Strategy

## Pipeline Overview

Two-stage pipeline:
1. **Stage 1 (Import/Clean):** Read sources → merge → save to DB
2. **Stage 2 (Analysis):** Read DB → filter → output rankings

## Stage 1: Import/Clean

```
INPUTS:
- estat_tgs00096.tsv.gz (population)
- NUTS2021.xlsx (mapping)
- Results/2021/*.zip (FUA boundaries)
- TCD_2015...tif (tree raster)

PROCESS:
1. Parse TSV → extract NUTS code + population
2. Parse NUTS2021.xlsx → NUTS2 → city name mapping
3. Match regions → merge population + FUA
4. Extract tree cover using FUA geometry
5. Save to SQLite DB

OUTPUT:
- regions table with: name, nuts_code, population, area_km2, tree_cover_km2, tree_cover_pct
```

## Stage 2: Analysis

```
INPUT: SQLite DB

PROCESS:
1. Query regions from DB
2. Filter by population threshold
3. Filter by major cities list

OUTPUT: Rankings by tree cover km2 and percentage
```

## Key Processing Steps

1. **Name Normalization:** Wien → vienna, Bruxelles → brussels, etc.
2. **FUA Matching:** Via normalized name matching (89 matched)
3. **Tree Extraction:** Clip raster to actual FUA geometry (not fixed buffer)