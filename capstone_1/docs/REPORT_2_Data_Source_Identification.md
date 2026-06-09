# Report 2: Data Source Identification

## Data Sources

| Source | File | Records | Description |
|--------|------|---------|------------|
| Population | estat_tgs00096.tsv.gz | 227 | Eurostat NUTS population |
| NUTS Mapping | NUTS2021.xlsx | 229 | NUTS2 to metro label |
| FUA Boundaries | Results/2021/*.zip | 768 | Urban Atlas 2021 |
| Tree Raster | TCD_2015_020m_eu_03035_d05_Full.tif | 1 | Copernicus TCD 2015 |

## Population Data

- **Source:** Eurostat TGS00096
- **Format:** TSV (tab-separated)
- **Years:** 2014-2025 (latest: 2024)
- **Geographic Units:** NUTS2 codes (e.g., AT13, DE11)

## NUTS Mapping

- **Source:** NUTS2021.xlsx - Metropolitan sheet
- **Purpose:** Maps NUTS codes to city/region names
- **Example:** AT13 → Wien (Vienna)

## FUA Boundaries

- **Source:** Copernicus Urban Atlas 2021
- **Format:** GeoPackage (.fgb) in ZIP files
- **Coverage:** 768 metropolitan areas

## Tree Raster

- **Source:** Copernicus Tree Cover Density 2015
- **Resolution:** 20m
- **Projection:** EPSG:3035 (ETRS89/LAEA)