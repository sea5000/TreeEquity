# Physical Data Model

## DBMS: SQLite 3

SQLite was chosen as the database management system because:

1. **Zero configuration** — No server setup required; the database is a single file.
2. **Self-contained** — The entire database (`.db` file) can be distributed with the project.
3. **Cross-platform** — Works identically on Windows, macOS, and Linux.
4. **Adequate for the data volume** — 433 records across 8 tables fits comfortably within SQLite's capabilities.
5. **Python native support** — The `sqlite3` module is part of Python's standard library.

## Database File

- **Path:** `data/kemv.db`
- **Size:** ~36 KB (after removing cell tower tables)
- **Encoding:** UTF-8
- **Journal Mode:** delete (default)

## SQL Schema

### Tables

```sql
CREATE TABLE countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    iso_code TEXT,
    area_km2 REAL,
    capital TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    nuts_code TEXT,
    population INTEGER,
    area_km2 REAL,
    tree_cover_km2 REAL,
    tree_cover_pct REAL
);

CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country_id INTEGER,
    capital TEXT,
    fua_code TEXT,
    population INTEGER,
    urban_area_km2 REAL,
    lat REAL,
    lon REAL,
    eTRS_x REAL,
    eTRS_y REAL,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    urban_area_fua_km2 REAL,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);

CREATE TABLE urban_trees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER NOT NULL,
    source_year INTEGER,
    tree_cover_pixels BLOB,
    tree_cover_km2 REAL,
    urban_mask_pixels BLOB,
    urban_mask_km2 REAL,
    tree_percentage REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

CREATE TABLE urban_trees_ua (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER NOT NULL,
    urban_km2 REAL,
    forest_km2 REAL,
    green_km2 REAL,
    tree_pct REAL,
    rank INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

CREATE TABLE city_rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_id INTEGER NOT NULL,
    pop_density REAL,
    tree_density REAL,
    pop_to_tree_ratio REAL,
    rank INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

CREATE TABLE population_annual (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    population_count INTEGER,
    FOREIGN KEY (country_id) REFERENCES countries(id),
    UNIQUE(country_id, year)
);

CREATE TABLE source_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    download_date DATE,
    record_count INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes

SQLite automatically creates an index for:
- Each `PRIMARY KEY` column (unique index)
- Each `UNIQUE` constraint

No additional indexes were explicitly defined due to the small data volume.

### Constraints

| Constraint Type | Example | Purpose |
|-----------------|---------|---------|
| PRIMARY KEY | `countries.id` | Uniquely identifies each row |
| FOREIGN KEY | `cities.country_id → countries.id` | Referential integrity |
| NOT NULL | `cities.name` | Ensures required fields |
| UNIQUE | `countries.name` | Prevents duplicate entries |
| UNIQUE composite | `population_annual(country_id, year)` | One record per country per year |
| DEFAULT | `cities.created_at` | Automatic timestamp on insert |

## Data Types Used

| SQLite Type | Usage | Rationale |
|-------------|-------|-----------|
| INTEGER | IDs, populations, years, counts | Exact numeric values |
| REAL | Areas, densities, percentages, coordinates | Floating-point measurements |
| TEXT | Names, codes, descriptions, timestamps | String data |
| BLOB | Pixel data arrays | Raw numpy arrays stored as binary |
| DATE | Download dates | Date values in ISO format |

## Physical Storage

The database file uses SQLite's default page size (4096 bytes) and is stored as a single file on disk. All tables use the default `B-tree` indexing structure.
