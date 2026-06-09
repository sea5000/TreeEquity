# Capstone Project 3 — Dashboard Development

## European Urban Tree Cover Analysis

Two interactive Flask dashboards analyzing tree equity across 28 European cities using data from Copernicus, Eurostat, and Wikipedia.

## Dashboards

| Dashboard | Type | Route | Purpose |
|---|---|---|---|
| **European Tree Cover Atlas** | Strategic | `/dashboard1` | High-level overview: map, top 10 cities, equity distribution, scatter plot, full ranking table |
| **City Tree Equity Analyzer** | Analytical | `/dashboard2` | Deep-dive: KPI cards, city comparison, pop-to-tree ratio ranking, density scatter, full equity table |

## Setup

```bash
source /home/spencer/.testvenv/bin/activate
python3 app.py
```

Open http://127.0.0.1:5050 in a browser.

## Deliverables

| Step | File |
|---|---|
| Step 1 — Dashboard Plan | `dashboard_plan.md` |
| Step 2 — SQL Queries | `sql/queries.sql` |
| Step 2 — DB Connection | `sql/db_connection.py` |
| Step 4 — Flask App | `app.py` |
| Step 4-5 — Dashboard 1 | `templates/dashboard1.html` |
| Step 4-5 — Dashboard 2 | `templates/dashboard2.html` |
| Step 4-5 — Styles | `static/style.css` |
| Step 6 — Screenshot D1 | `screenshots/dashboard1.png` |
| Step 6 — Screenshot D2 | `screenshots/dashboard2.png` |
| Step 6 — UX Notes | `screenshots/ux_notes.md` |

## Tech Stack

- **Backend:** Flask + sqlite3 (Python standard library)
- **Frontend:** HTML5, CSS3, Chart.js (CDN)
- **Database:** SQLite 3 (from Capstone 2, at `capstone_1/data/kemv.db`)
