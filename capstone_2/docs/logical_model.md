# Logical Data Model

## Overview

The logical model translates the conceptual entities into a relational schema in Third Normal Form (3NF). All entities are decomposed to eliminate redundancy while preserving data integrity through primary and foreign key constraints.

## Normalization

### 1NF (First Normal Form)
All tables have atomic column values. Multi-valued attributes (e.g., a country having multiple cities) are handled through separate tables with foreign keys rather than repeating groups.

### 2NF (Second Normal Form)
All tables have a single-column primary key. No partial dependencies exist because no table has a composite primary key. The `population_annual` table uses `(country_id, year)` as a unique constraint rather than a composite PK, with a surrogate `id` as the primary key.

### 3NF (Third Normal Form)
All non-key attributes are functionally dependent on the primary key only:
- `cities.name` depends on `cities.id` (not on `country_id`)
- `urban_trees.tree_percentage` depends on `urban_trees.id` (derived from tree_cover_km2 / urban_mask_km2, but stored for query performance)
- `city_rankings.rank` depends on `city_rankings.id` (computed from tree_density across all cities, but stored as a materialized value)

## Entity Relationship Diagram

See `logical_erd.puml` for the visual diagram.

## Table Definitions

### countries
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique country identifier |
| name | TEXT | NOT NULL, UNIQUE | Country name |
| iso_code | TEXT | | ISO 3166-1 alpha-2 code |
| area_km2 | REAL | | Total land area in km² |
| capital | TEXT | | Capital city name |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Row creation timestamp |

### regions
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique region identifier |
| name | TEXT | | Region/city name (may be NUTS code if unmapped) |
| nuts_code | TEXT | | NUTS2 statistical code |
| population | INTEGER | | Population from latest Eurostat year |
| area_km2 | REAL | | Functional Urban Area in km² |
| tree_cover_km2 | REAL | | Tree cover area in km² |
| tree_cover_pct | REAL | | Tree cover as percentage of area |

### cities
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique city identifier |
| name | TEXT | NOT NULL | City name |
| country_id | INTEGER | FK → countries.id | Owning country |
| capital | TEXT | | Capital status description |
| fua_code | TEXT | | Functional Urban Area code |
| population | INTEGER | | City population |
| urban_area_km2 | REAL | | Urban area extent in km² |
| lat | REAL | | Latitude (WGS84) |
| lon | REAL | | Longitude (WGS84) |
| eTRS_x | REAL | | ETRS89/LAEA easting |
| eTRS_y | REAL | | ETRS89/LAEA northing |
| source | TEXT | | Data source identifier |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Row creation timestamp |
| urban_area_fua_km2 | REAL | | FUA-derived urban area in km² |

### urban_trees
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique measurement identifier |
| city_id | INTEGER | FK → cities.id, NOT NULL | Measured city |
| source_year | INTEGER | | Year of the tree cover raster |
| tree_cover_pixels | BLOB | | Raw pixel count of tree cover |
| tree_cover_km2 | REAL | | Tree cover area in km² |
| urban_mask_pixels | BLOB | | Raw pixel count of urban mask |
| urban_mask_km2 | REAL | | Urban mask area in km² |
| tree_percentage | REAL | | Tree cover as % of urban area |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Row creation timestamp |

### urban_trees_ua
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique classification identifier |
| city_id | INTEGER | FK → cities.id, NOT NULL | Classified city |
| urban_km2 | REAL | | Urban land area in km² |
| forest_km2 | REAL | | Forest land area in km² |
| green_km2 | REAL | | Green urban area in km² |
| tree_pct | REAL | | Tree cover percentage |
| rank | INTEGER | | Rank by tree percentage |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Row creation timestamp |

### city_rankings
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique ranking identifier |
| city_id | INTEGER | FK → cities.id, NOT NULL | Ranked city |
| pop_density | REAL | | Population density (people/km²) |
| tree_density | REAL | | Tree cover density (km² tree/km² urban) |
| pop_to_tree_ratio | REAL | | Population per km² of tree cover |
| rank | INTEGER | | Overall rank (1 = best tree equity) |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Row creation timestamp |

### population_annual
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique record identifier |
| country_id | INTEGER | FK → countries.id, NOT NULL | Country |
| year | INTEGER | NOT NULL | Calendar year |
| population_count | INTEGER | | Population for that year |

### source_metadata
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique source identifier |
| source_name | TEXT | NOT NULL | Name of the data source |
| download_date | DATE | | Date the data was downloaded |
| record_count | INTEGER | | Number of records obtained |
| notes | TEXT | | Additional documentation |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Row creation timestamp |

## Foreign Key Relationships

| Source Table | FK Column | Target Table | Description |
|-------------|-----------|-------------|-------------|
| cities | country_id | countries | City belongs to a country |
| urban_trees | city_id | cities | Tree cover measurement belongs to a city |
| urban_trees_ua | city_id | cities | Land cover classification belongs to a city |
| city_rankings | city_id | cities | Ranking belongs to a city |
| population_annual | country_id | countries | Population record belongs to a country |
