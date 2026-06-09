# Capstone Project 3 — Dashboard Plan

## Case Study

**How does urban tree canopy cover relate to population density across European cities?**

This project analyzes the relationship between population density, tree canopy cover, and overall tree equity across 28 major European cities. Using data from Copernicus (Tree Cover Density 2015 raster), Eurostat (population statistics), and Wikipedia (city data), we built a normalized SQLite database to explore which cities provide the best access to tree cover relative to their population density.

**Equity Categorization:** Cities are classified into four equity tiers based on their population-to-tree ratio (people per km² of tree cover), using data-driven quartile cutoffs:
- **Excellent** (<64,000 people/km² tree cover) — low population pressure on canopy
- **Good** (64,000–142,000) — moderate pressure
- **Fair** (142,000–250,000) — elevated pressure
- **Needs Improvement** (>250,000) — high population pressure, low canopy relative to population

The central question: *Which European cities have the best — and worst — balance between people and trees?*

---

## Dashboard 1: European Tree Cover Atlas (Strategic)

### Dashboard Type
**Strategic** — Designed for high-level overview and monitoring. This dashboard gives decision-makers a bird's-eye view of tree equity across Europe, identifying which cities and countries are performing well and which need attention.

### Target Users
- **Urban planners** seeking regional benchmarks for tree cover targets
- **Policy makers** at EU or national level allocating green infrastructure funding
- **Environmental advocates** communicating tree equity disparities to the public

### Target User Demographics
- Professional background: government, academia, non-profit
- Technical comfort: moderate — needs clear, intuitive charts without requiring data expertise
- Decision-making context: strategic planning, resource allocation, public reporting

### Story
*"Trees are not evenly distributed across European cities. While some cities like Bern (7.08%) and Dublin (6.74%) offer generous canopy cover, others like Rome (0.44%) and Prague (0.18%) leave their residents with minimal green space. When weighted by population density, the disparities grow even starker — Paris has 205 people per hectare but only 2.13% tree cover. This dashboard reveals where Europe's urban forests thrive and where they need investment."*

### Key Metrics
- Tree cover percentage (% of urban area)
- Tree cover area (km²)
- Population
- Population density (people/km²)
- Tree equity rank (1 = best)
- Population-to-tree ratio (people per km² of tree cover)
- Equity category (Excellent / Good / Fair / Needs Improvement)

### Visualizations (5 total)

| # | Visualization | Type | Purpose |
|---|---|---|---|
| 1 | **Interactive Leaflet map** — OpenStreetMap tiles with city circle markers colored by equity category, sized by population, with click popups showing city details | Qualitative (geospatial) | Show geographic distribution of tree equity on a real map |
| 2 | **Bar chart** — Top 10 cities by tree cover percentage | Quantitative (bar) | Identify best-performing cities at a glance |
| 3 | **Scatter plot** — Population vs Tree Cover %, points colored by equity category | Quantitative (scatter) | Reveal the relationship between city size and canopy cover |
| 4 | **Donut chart** — Breakdown of cities by equity category | Quantitative (pie/donut) | Show proportion of cities in each equity tier |
| 5 | **Data table** — All 28 ranked cities with sortable columns | Qualitative (table) | Enable detailed comparison and data export |

### Interactive Elements
- **Country filter dropdown** — filter all visualizations by country
- **Equity category filter** — show only Excellent / Good / Needs Improvement cities
- **City search** — find and highlight a specific city

---

## Dashboard 2: City Tree Equity Analyzer (Analytical)

### Dashboard Type
**Analytical** — Designed for deep exploration and comparison. This dashboard lets researchers and analysts investigate specific cities, compare them side-by-side, and understand the underlying drivers of tree equity.

### Target Users
- **Environmental researchers** studying urban forestry patterns
- **Data analysts** at city governments evaluating local tree cover programs
- **Journalists** researching stories on environmental inequality

### Target User Demographics
- Professional background: research, data science, journalism
- Technical comfort: high — comfortable with interactive filtering and multi-dimensional data
- Decision-making context: detailed analysis, report generation, hypothesis testing

### Story
*"Tree equity is not just about how many trees a city has — it's about how those trees serve the people who live there. A small city like Bern can have high tree cover but low population, while a dense metropolis like Paris struggles to balance development with greenery. This dashboard lets you explore the trade-offs: compare any two cities across tree percentage, population density, and equity rank to understand what drives the numbers."*

### Key Metrics
- Tree cover percentage (%)
- Population density (people/km²)
- Population-to-tree ratio (people per km² of tree cover)
- Tree equity rank
- Tree density (km² tree cover per km² urban area)

### Visualizations (5 total)

| # | Visualization | Type | Purpose |
|---|---|---|---|
| 1 | **KPI cards** — Selected city shows tree %, rank, pop density, pop-to-tree ratio as large readable numbers | Qualitative (metric cards) | Give immediate snapshot of a city's key stats |
| 2 | **Horizontal bar chart** — All cities ranked by population-to-tree ratio (lower = better), color-coded by equity category | Quantitative (horizontal bar) | Show which cities have the most people competing for each km² of tree cover |
| 3 | **Scatter plot** — Population density vs Tree density with trend line | Quantitative (scatter) | Reveal the density-canopy trade-off across all cities |
| 4 | **Grouped bar chart** — Compare 2 selected cities side-by-side on 4 metrics (tree %, pop density, equity rank, pop-to-tree ratio) | Quantitative (grouped bar) | Enable direct city-to-city comparison |
| 5 | **Equity ranking table** — Full 28-city table with color-coded rows by equity category, sortable by any column | Qualitative (table) | Provide complete reference data with visual cues |

### Interactive Elements
- **City multi-select dropdown** — pick 1-2 cities to highlight/compare
- **Population range slider** — filter cities by minimum population
- **Equity category checkboxes** — toggle visibility of Excellent/Good/Fair/Needs Improvement cities
- **Sortable table columns** — click column headers to reorder

---

## Quantitative Visualization Techniques Used (6 total, ≥4 required)

| Technique | Dashboard | Description |
|---|---|---|
| Bar chart | D1 | Top 10 tree cover percentages |
| Scatter plot | D1, D2 | Population vs tree %; density vs tree density |
| Donut/pie chart | D1 | Equity category distribution |
| Horizontal bar chart | D2 | Pop-to-tree ratio ranking |
| Grouped bar chart | D2 | City comparison on multiple metrics |
| (Metrics/numbers) | D2 | KPI cards with large numerical display |

## Qualitative Visualization Techniques Used (5 total, ≥3 required)

| Technique | Dashboard | Description |
|---|---|---|
| Geospatial map | D1 | City markers positioned by coordinates |
| Data tables | D1, D2 | Full city listings with sortable columns |
| KPI metric cards | D2 | At-a-glance city statistics |
| Color-coded categories | D1, D2 | Equity category as visual color coding |
| Interactive filters | D1, D2 | Dropdowns, sliders, checkboxes, search |
