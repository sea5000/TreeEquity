# Conceptual Data Model

## Overview

The conceptual model describes the high-level entities and relationships for the European Urban Tree Cover analysis. The model captures the connection between population centers, administrative regions, and environmental measurements.

## Entities (8)

### 1. Country
A sovereign European nation. Countries contain NUTS regions and cities, and maintain annual population records.

**Attributes:** name, ISO code, area (km²), capital city

### 2. NUTS Region
A NUTS2 statistical region defined by Eurostat. These are the primary analytical units for tree cover comparison. Some regions are metropolitan (mapped to a city name) while others are non-metropolitan.

**Attributes:** name, NUTS code, population, area (km²), tree cover (km²), tree cover (%)

### 3. City
A major European urban center. Cities serve as the link between population data and environmental measurements.

**Attributes:** name, population, urban area (km²), coordinates (latitude/longitude + ETRS projection), FUA code

### 4. Urban Tree Canopy
Tree cover measurements derived from the Copernicus Tree Cover Density 2015 raster at 20m resolution. Represents actual tree canopy within the urban footprint.

**Attributes:** tree cover pixels, tree cover (km²), urban mask pixels, urban mask (km²), tree percentage, source year

### 5. Urban Atlas Land Cover
Land cover classification from the Copernicus Urban Atlas 2021. Provides broader context including forest and green urban areas.

**Attributes:** urban area (km²), forest area (km²), green urban area (km²), tree percentage, rank

### 6. City Ranking
Derived metrics ranking cities by tree density and population-to-tree ratios.

**Attributes:** population density, tree density, population-to-tree ratio, rank

### 7. Population Record
Annual population counts for each country.

**Attributes:** year, population count

### 8. Data Source
Metadata documenting the origin of each dataset used in the project.

**Attributes:** source name, download date, record count, notes

## Relationships

| Relationship | Type | Description |
|-------------|------|-------------|
| Country → NUTS Region | 1:M | A country contains multiple NUTS regions |
| Country → City | 1:M | A country contains multiple cities |
| Country → Population Record | 1:M | A country has annual population records |
| NUTS Region → City | 1:M | A region contains multiple cities (conceptual) |
| City → Urban Tree Canopy | 1:1 | A city has one tree cover measurement |
| City → Urban Atlas Land Cover | 1:1 | A city has one land cover classification |
| City → City Ranking | 1:1 | A city has one ranking entry |
| Data Source → (all entities) | M:N | Each source documents multiple entities |

## Why This Model

This model is suitable because it:

1. **Separates administrative units** (Country, NUTS Region) from **physical measurements** (Urban Tree Canopy, Urban Atlas Land Cover), allowing analysis at different geographic granularities.
2. **Links population data** (Population Record, City) to **environmental data** (tree cover, land cover), enabling the core research question about population vs. tree cover equity.
3. **Maintains data provenance** through the Data Source entity, supporting reproducibility.
4. **Supports hierarchical analysis** — from country-level → regional-level → city-level, with consistent foreign key relationships.
