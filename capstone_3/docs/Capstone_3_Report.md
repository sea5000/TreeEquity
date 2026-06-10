# Capstone 3 Report: Dashboard Development

## European Urban Tree Cover Analysis

---

## Deliverables Overview

| Step | Deliverable | File |
|------|-------------|------|
| Step 1 | Dashboard Plan | `dashboard_plan.md` |
| Step 2 | Database Connection & SQL Queries | `sql/queries.sql`, `sql/db_connection.py` |
| Step 3 | N/A | — |
| Step 4–5 | Dashboard Code & Screenshots | `app.py`, `templates/*.html`, `static/style.css` |
| Step 6 | UX Notes & Testing | `screenshots/ux_notes.md` |

---

## Step 1: Dashboard Plan

### Case Study

How does urban tree canopy cover relate to population density across European cities? This project analyzes the relationship between population density, tree canopy cover, and tree equity across 98 cities in 42 European countries.

### Equity Categorization

Cities are classified into four equity tiers based on quartile breaks of the population-to-tree ratio (people per km² of tree cover):

| Category | Ratio Range | Cities |
|----------|-------------|--------|
| Excellent | <50,844 | 25 |
| Good | 50,844–134,561 | 25 |
| Fair | 134,561–236,415 | 24 |
| Needs Improvement | >236,415 | 24 |

### Dashboard Types

| Dashboard | Type | Purpose | Route |
|-----------|------|---------|-------|
| European Tree Cover Atlas | Strategic | High-level geographic overview and monitoring | `/dashboard1` |
| City Tree Equity Analyzer | Analytical | Deep-dive comparison and exploration | `/dashboard2` |

### Visualization Techniques

**Quantitative (6 total, ≥4 required):**
- Bar chart (D1 — top 10 tree cover %)
- Scatter plot (D1, D2 — population vs tree %, density vs tree density)
- Donut chart (D1 — equity category distribution)
- Horizontal bar chart (D2 — pop-to-tree ratio ranking)
- Grouped bar chart (D2 — city comparison across 4 metrics)
- KPI metric cards (D2 — numerical display)

**Qualitative (5 total, ≥3 required):**
- Geospatial map (D1 — Leaflet map with equity-colored markers)
- Sortable data tables (D1, D2 — full city listings)
- KPI metric cards (D2 — at-a-glance stats)
- Color-coded equity categories (D1, D2 — consistent green/yellow/red)
- Interactive filters (D1, D2 — dropdowns, sliders, checkboxes, search)

---

## Step 2: Database Integration

### Database Source

The database from Capstone 2 (`capstone_1/data/kemv.db`) was expanded with a new `city_tree_rankings` table containing 98 cities across 42 countries. This table combines data from the original `cities`, `countries`, `urban_trees`, and `city_rankings` tables into a single flat structure optimized for dashboard queries.

### Database Connection

File: `sql/db_connection.py`

- SQLite connection with row factory for dictionary access
- PRAGMA optimizations: `journal_mode=WAL`, `cache_size=-8000` (64 MB)
- 7 query functions for dashboard data retrieval

### SQL Queries

File: `sql/queries.sql`

| Query | Purpose | Tables Joined |
|-------|---------|---------------|
| All Cities with Full Metrics | Map, tables, charts | 4 (cities + countries + urban_trees + city_rankings) |
| Top 10 by Tree Cover % | D1 bar chart | 3 |
| Equity Category Distribution | D1 donut chart | 1 (city_rankings) |
| Countries List | D1 filter dropdown | 2 |
| Filtered Cities by Country | D1 country filter | 4 |
| Single City Detail | D2 KPI cards | 4 |
| Filtered by Population + Equity | D2 tables/charts | 4 |

> The `db_connection.py` queries an additional `city_tree_rankings` table (not present in the Capstone 2 schema) for the main `/api/cities` endpoint, while the remaining functions query the original normalized tables.

---

## Step 4–5: Dashboard Implementation

### Tech Stack

- **Backend:** Flask (Python) + sqlite3
- **Frontend:** HTML5, CSS3, Chart.js 4.4.7 (CDN), Plotly.js (CDN), Leaflet 1.9.4 (CDN)
- **Database:** SQLite 3

### Application Structure

```
capstone_3/
├── app.py                  # Flask application (routes + API endpoints)
├── dashboard_plan.md       # Step 1 deliverable
├── sql/
│   ├── db_connection.py    # Database connection and query functions
│   └── queries.sql         # SQL query reference
├── templates/
│   ├── dashboard1.html     # European Tree Cover Atlas
│   └── dashboard2.html     # City Tree Equity Analyzer
├── static/
│   └── style.css           # Global styles
└── screenshots/
    ├── dashboard1.png      # D1 screenshot
    ├── dashboard2.png      # D2 screenshot
    └── ux_notes.md         # Step 6 UX documentation
```

### API Endpoints

| Endpoint | Method | Returns |
|----------|--------|---------|
| `/` | GET | Redirects to Dashboard 1 |
| `/dashboard1` | GET | Dashboard 1 HTML |
| `/dashboard2` | GET | Dashboard 2 HTML |
| `/api/cities` | GET | All 98 cities with metrics |
| `/api/top10` | GET | Top 10 by tree cover % |
| `/api/equity-distribution` | GET | Counts per equity category |
| `/api/countries` | GET | Country list for filters |
| `/api/city-detail?name=` | GET | Single city detail |
| `/api/filtered-cities?...` | GET | Filtered city list |

### Dashboard 1: European Tree Cover Atlas (Strategic)

**Target Users:** Urban planners, policy makers, environmental advocates

**Visualizations:**
1. **Leaflet map** — City markers colored by equity category, sized by population, with click popups
2. **Summary stat cards** — City count, avg tree cover %, best/worst city
3. **Donut chart** — Equity category distribution (Chart.js)
4. **Bar chart** — Top 10 cities by tree cover % (horizontal, Chart.js)
5. **Scatter plot** — Population vs tree cover %, colored by equity (Chart.js)
6. **Box plot** — Population-to-tree ratio distribution with quartile bands (Plotly)
7. **Sortable data table** — All cities with rank, tree %, density, ratio

**Interactive Elements:**
- Country dropdown filter
- Equity category dropdown filter
- City search text input

### Dashboard 2: City Tree Equity Analyzer (Analytical)

**Target Users:** Researchers, data analysts, journalists

**Visualizations:**
1. **KPI cards** — Selected city name, tree %, equity rank, population density
2. **Horizontal bar chart** — All cities ranked by pop-to-tree ratio (Chart.js)
3. **Scatter plot** — Population density vs tree density (Chart.js)
4. **Grouped bar chart** — Compare 1–2 cities across 4 metrics (normalized %, Chart.js)
5. **Sortable equity ranking table** — Full dataset with color-coded rows

**Interactive Elements:**
- Multi-select city dropdown (Ctrl+click)
- Population range slider (dual input)
- Equity category checkboxes
- Sortable table columns

---

## Step 6: User Experience & Testing

### UX Improvements

1. **Responsive layout** — CSS Grid/Flexbox; 2-column desktop, single-column mobile
2. **Consistent color coding** — Green/yellow/red equity categories across all charts, map, and tables
3. **Equity badges** — Pill-shaped labels for quick scanning in tables
4. **Tooltip information** — All charts show city name, country, and metrics on hover
5. **Single API call** — Dashboard 1 loads all data once and filters client-side
6. **Chart reuse** — Destroys/recreates chart instances to prevent memory leaks

### Key Performance Optimizations

- SQLite WAL mode and 64 MB cache for faster queries
- Client-side filtering for instant responsiveness
- Single API call for Dashboard 1 (98 cities loaded once)

---

## Key Findings

| Metric | Value |
|--------|-------|
| Cities analyzed | 98 |
| Countries represented | 42 |
| Average tree cover | 3.27% |
| Best tree cover | Vatican City (16.90%) |
| Worst tree cover | Reggio Calabria (0.01%) |
| Largest city | London (8.98M) |
| Smallest city | Vatican City (800) |
| Dataset expanded from | 30 cities (Capstone 2) → 98 cities (Capstone 3) |

### Top 10 Cities by Tree Cover %

| Rank | City | Country | Tree % |
|------|------|---------|--------|
| 1 | Vatican City | Vatican City | 16.90% |
| 2 | San Marino | San Marino | 8.25% |
| 3 | Bern | Switzerland | 7.08% |
| 4 | Reykjavik | Iceland | 6.77% |
| 5 | Dublin | Ireland | 6.74% |
| 6 | Merida | Spain | 6.70% |
| 7 | Tallinn | Estonia | 6.68% |
| 8 | Bremen | Germany | 6.55% |
| 9 | Riga | Latvia | 6.54% |
| 10 | Leipzig | Germany | 6.52% |

---

## Files

| File | Description |
|------|-------------|
| `app.py` | Flask application with 8 API endpoints |
| `templates/dashboard1.html` | Dashboard 1: European Tree Cover Atlas |
| `templates/dashboard2.html` | Dashboard 2: City Tree Equity Analyzer |
| `static/style.css` | Global styles and responsive layout |
| `sql/db_connection.py` | SQLite connection and 7 query functions |
| `sql/queries.sql` | Reference SQL queries |
| `dashboard_plan.md` | Step 1 — Dashboard plan and design |
| `screenshots/ux_notes.md` | Step 6 — UX improvements and testing |
