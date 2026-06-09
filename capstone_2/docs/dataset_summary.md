# Dataset Summary

## Case Study

**How do European NUTS2 regions compare in urban tree cover relative to their population?**

This project analyzes the relationship between population density and tree canopy cover across European metropolitan regions, using data from Copernicus (tree cover density, urban land cover), Eurostat (population), and Wikipedia (city data).

## Dataset Structure

The database contains 8 tables with a total of 433 records across all entities.

### Entities Overview

| Entity | Table | Rows | Description |
|--------|-------|------|-------------|
| Country | `countries` | 51 | European countries with ISO codes and area |
| NUTS Region | `regions` | 212 | NUTS2 regions with population and tree cover |
| City | `cities` | 30 | Major European cities with coordinates |
| Urban Tree Canopy | `urban_trees` | 30 | Tree cover from Copernicus TCD 2015 raster |
| Urban Atlas Land Cover | `urban_trees_ua` | 29 | Land cover classification from Urban Atlas 2021 |
| City Ranking | `city_rankings` | 28 | Rankings based on tree density metrics |
| Population Record | `population_annual` | 51 | Annual population counts by country |
| Data Source | `source_metadata` | 2 | Metadata about data sources |

### Key Attributes

- **NUTS Regions:** name, NUTS code, population, area (km²), tree cover (km² and %)
- **Cities:** name, population, urban area (km²), coordinates (lat/lon + ETRS projection)
- **Urban Tree Canopy:** tree cover pixels, tree cover km², tree percentage (from 20m resolution TCD raster)
- **Urban Atlas Land Cover:** urban area, forest area, green urban area, tree percentage
- **City Rankings:** population density, tree density, population-to-tree ratio, rank

## Data Sources

| Source | Description | Records |
|--------|-------------|---------|
| Eurostat TGS00096 | NUTS population data (2014–2024) | 227 regions |
| Copernicus Urban Atlas 2021 | FUA boundaries in GeoPackage format | 768 metropolitan areas |
| Copernicus TCD 2015 | Tree Cover Density raster at 20m resolution | 1 raster covering EU |
| NUTS2021 | NUTS classification with metropolitan labels | 229 entries |
| Wikipedia | European country and city data | 51 countries, 30 cities |
