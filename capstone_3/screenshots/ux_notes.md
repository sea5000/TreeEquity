# Step 6 — User Experience (UX) Considerations & Testing

## UX Improvements Implemented

### 1. Responsive Layout
- CSS Grid and Flexbox used throughout both dashboards
- On screens wider than 900px: charts display side-by-side in a 2-column grid
- On screens narrower than 900px: charts stack vertically for readability
- KPI cards: 4-column on desktop, 2-column on tablet, single-column on mobile

### 2. Chart Readability
- **Color-coded equity categories** — consistent green/yellow/red color scheme across all charts, tables, and the map, making equity status immediately recognizable
- **Equity badges** — pill-shaped labels with colored backgrounds in tables for quick scanning
- **Tooltip information** — all Chart.js charts display city name, country, and relevant values on hover
- **Horizontal bar chart** — Top 10 tree cover cities uses horizontal bars for easier reading of city names
- **Equity ranking table** — color-coded left border (green/yellow/red) for each row

### 3. Interactive Elements
- **Dashboard 1** — Country dropdown filter, equity category dropdown, city search text input — all update every chart and table simultaneously
- **Dashboard 2** — Multi-select city dropdown (Ctrl+click for multiple), population range slider with live label updates, equity category checkboxes
- **Sortable tables** — click column headers on either dashboard to sort ascending/descending
- **Chart highlighting** — selected cities in Dashboard 2 are highlighted with dark green borders on horizontal bar chart and larger markers on scatter plot

### 4. Performance Optimization
- **SQLite PRAGMA settings** — `journal_mode=WAL` and `cache_size=-8000` (64MB cache) applied on each connection for faster queries
- **Single API call** — Dashboard 1 loads all city data in one `/api/cities` call and filters client-side, avoiding redundant server requests
- **Client-side filtering** — country, equity, and search filters operate on already-loaded data for instant responsiveness
- **Chart.js reuse** — chart instances are destroyed and recreated on filter change (prevents memory leaks from stale charts)

### 5. Data Loading
- **Loading states** — summary stats display `--` until data loads; tables remain empty until fetch completes
- **Static data** — since the dataset is static (2015 tree measurements, 2025 population projections), no real-time updates are needed. Data loads once on page load.

### 6. Navigation
- **Top navigation bar** — both dashboards include links to switch between Atlas and Analyzer views
- **Consistent header** — green gradient header with title, subtitle, and navigation appears on both dashboards

## User Feedback (Simulated Peer Review)

| Feedback | Action Taken |
|---|---|
| "The map could use labels for cities" | Added custom tooltip on hover showing city name, country, and tree cover % |
| "Hard to compare cities side-by-side" | Added city selector in Dashboard 2 with comparison bar chart for 4 metrics |
| "I want to see only certain equity categories" | Added equity category dropdown (D1) and checkboxes (D2) |
| "The scatter plot points are too small" | Increased point radius and made selected cities more prominent with border |
| "Tables need sorting" | Added click-to-sort on all table column headers |

## Known Limitations
- Population range slider uses two separate `<input type="range">` elements rather than a dual-handle slider (simpler implementation, adequate for the 28-city dataset)
- Leaflet map loads OpenStreetMap tiles from the internet; requires internet connectivity for the map background to display
