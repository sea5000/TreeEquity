# TreeEquity — European Urban Tree Cover Analysis

A three-part capstone project analyzing **urban tree equity** across European cities — from raw satellite
and statistical data to a production-style interactive dashboard. It answers a simple but important
question:

> **How does urban tree canopy cover relate to population density (and tree equity) across European cities?**

The project was delivered in three linked capstone stages, each building on the last: data collection and
cleaning → relational database design → an interactive web dashboard.

---

## The three capstones

### 1. Capstone 1 — Data Collection & Cleaning (`capstone_1/`)

Built a geospatial data pipeline that combines population, administrative boundaries, and satellite-derived
tree cover into a single dataset.

- **Inputs**
  - Eurostat NUTS population data (`estat_tgs00096`)
  - Copernicus **Tree Cover Density 2015** raster (20 m resolution)
  - Copernicus **Urban Atlas 2021** Functional Urban Area (FUA) boundaries
  - NUTS2021 metropolitan-name mapping
- **Process** (`import_data.py`) — parse the Eurostat TSV, map NUTS codes to city names, match cities to
  their Urban Atlas FUA polygons (via normalized-name matching), clip the tree raster to each *actual*
  FUA boundary, and compute tree cover in km² and %.
- **Analysis** (`analysis.py`) — rank regions by tree cover km² and percentage.
- **Output** — a SQLite database of regions, later expanded into the full city dataset.

**Results:** 212 regions loaded, 89 with tree-cover data extracted from their real FUA boundaries
(≈10 minutes to process).

### 2. Capstone 2 — Relational Database Design (`capstone_2/`)

Designed and documented a normalized **SQLite** schema (3NF) that cleanly separates administrative units,
physical measurements, derived metrics, and source metadata.

- **8 core tables:** `countries`, `regions`, `cities`, `urban_trees` (Copernicus TCD raster metrics),
  `urban_trees_ua` (Urban Atlas land cover), `city_rankings` (tree-density and population-to-tree metrics),
  `population_annual`, and `source_metadata`.
- **Documentation:** conceptual, logical, and physical data models plus ER diagrams (PlantUML + PNG).
- The database underpins the dashboard and was extended with a flat `city_tree_rankings` table (98 cities,
  42 countries) in Capstone 3.

### 3. Capstone 3 — Dashboard Development (`capstone_3/`)

Two interactive **Flask** dashboards visualising tree equity using Chart.js, Plotly, and Leaflet against the
SQLite database from Capstone 2.

| Dashboard | Type | Route | Purpose |
|---|---|---|---|
| **European Tree Cover Atlas** | Strategic | `/dashboard1` | High-level overview: Leaflet map, summary stat cards, equity donut, top-10 bar chart, population–tree scatter + box plot, full sortable table |
| **City Tree Equity Analyzer** | Analytical | `/dashboard2` | Deep-dive: KPI cards, pop-to-tree ratio rankings, density scatter, grouped city comparison, color-coded equity table |

Cities are classified into four **equity tiers** by quartile breaks of the population-to-tree ratio
(people per km² of tree cover): **Excellent · Good · Fair · Needs Improvement**.

**Key findings**

| Metric | Value |
|---|---|
| Cities analyzed | 98 |
| Countries represented | 42 |
| Average tree cover | 3.27% |
| Best tree cover | Vatican City — 16.90% |
| Worst tree cover | Reggio Calabria — 0.01% |
| Dataset growth | 30 cities (Cap. 2) → 98 cities (Cap. 3) |

---

## Repository layout

```
capstone_1/            # Data collection & cleaning pipeline
├── import_data.py     # Builds the geospatial dataset (Eurostat + Copernicus)
├── analysis.py        # Ranks regions by tree cover
└── docs/              # Capstone 1 report + sub-reports
capstone_2/            # Relational database design
├── docs/              # Conceptual / logical / physical models, ER diagrams
└── sql/queries.sql    # Reference queries
capstone_3/            # Interactive dashboard
├── app.py             # Flask app + API endpoints
├── dashboard_plan.md  # Step 1 — design
├── sql/               # db_connection.py + queries.sql + import_city_rankings.py
├── templates/         # dashboard1.html, dashboard2.html
├── static/style.css
└── screenshots/       # Dashboard screenshots + UX notes
Capstone Project 2.pdf # Capstone 2 report
Capstone Project 3.pdf # Capstone 3 report
template.md            # Academic writing template for the reports
```

The raw geospatial data files (Eurostat TSV, Copernicus raster/FUA zips, etc.) are large and are kept out
of version control.

---

## Running the dashboard

```bash
# With the required Python environment and the SQLite DB in place:
python3 capstone_3/app.py
```

Then open the printed local URL (default http://127.0.0.1:5050).

**Tech stack**

| Layer | Tools |
|---|---|
| Capstone 1 | Python · `rasterio` · `fiona` · `numpy` · `pandas` · `shapely` |
| Capstone 2 | SQLite 3 · normalized (3NF) schema · PlantUML for ER diagrams |
| Capstone 3 | Flask · sqlite3 · Chart.js · Plotly · Leaflet · HTML5/CSS3 |

---

## Capstone reports

Full write-ups live in the repo:

- `capstone_1/docs/Capstone_1_Report.md` — case study selection, data sources, collection strategy,
  pipeline implementation, and cleaning
- `capstone_2/docs/Capstone 2 Report.md` — conceptual, logical, and physical data models
- `capstone_3/docs/Capstone_3_Report.md` (+ `capstone_3/README.md`) — dashboard plan, API, and UX notes

The capstone PDFs are also available at the repo root and in each `docs/` folder.