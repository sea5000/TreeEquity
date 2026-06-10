import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "capstone_1" / "data" / "kemv.db"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA cache_size=-8000")
    return conn


def query_all_cities():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            id AS city_id,
            city AS city_name,
            country,
            population,
            urban_area_km2,
            lat,
            lon,
            ROUND(tree_percentage, 2) AS tree_pct,
            ROUND(tree_cover_km2, 2) AS tree_km2,
            ROUND(population_density, 0) AS pop_density,
            ROUND(tree_density_per_km2, 6) AS tree_density,
            ROUND(pop_to_tree_ratio, 0) AS pop_to_tree_ratio,
            rank AS equity_rank
        FROM city_tree_rankings
        ORDER BY rank ASC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def query_top10_tree_pct():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            ci.name AS city_name,
            c.name AS country,
            ROUND(ut.tree_percentage, 2) AS tree_pct
        FROM cities ci
        JOIN countries c ON c.id = ci.country_id
        JOIN urban_trees ut ON ut.city_id = ci.id
        ORDER BY ut.tree_percentage DESC
        LIMIT 10
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def query_equity_distribution():
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            CASE
                WHEN cr.pop_to_tree_ratio < 64000 THEN 'Excellent'
                WHEN cr.pop_to_tree_ratio < 142000 THEN 'Good'
                WHEN cr.pop_to_tree_ratio < 250000 THEN 'Fair'
                ELSE 'Needs Improvement'
            END AS equity_category,
            COUNT(*) AS city_count
        FROM city_rankings cr
        GROUP BY equity_category
        ORDER BY MIN(cr.pop_to_tree_ratio) ASC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def query_countries():
    conn = get_connection()
    rows = conn.execute("""
        SELECT DISTINCT c.name AS country_name, c.iso_code
        FROM countries c
        JOIN cities ci ON ci.country_id = c.id
        ORDER BY c.name
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def query_city_detail(city_name):
    conn = get_connection()
    row = conn.execute("""
        SELECT
            ci.name AS city_name,
            c.name AS country,
            ci.population,
            ci.urban_area_km2,
            ROUND(ut.tree_percentage, 2) AS tree_pct,
            ROUND(ut.tree_cover_km2, 2) AS tree_km2,
            ROUND(cr.pop_density, 0) AS pop_density,
            ROUND(cr.tree_density, 6) AS tree_density,
            ROUND(cr.pop_to_tree_ratio, 0) AS pop_to_tree_ratio,
            (SELECT COUNT(*) FROM city_rankings) + 1 - cr.rank AS equity_rank,
            CASE
                WHEN cr.pop_to_tree_ratio < 64000 THEN 'Excellent'
                WHEN cr.pop_to_tree_ratio < 142000 THEN 'Good'
                WHEN cr.pop_to_tree_ratio < 250000 THEN 'Fair'
                ELSE 'Needs Improvement'
            END AS equity_category,
            ci.lat,
            ci.lon
        FROM cities ci
        JOIN countries c ON c.id = ci.country_id
        JOIN urban_trees ut ON ut.city_id = ci.id
        JOIN city_rankings cr ON cr.city_id = ci.id
        WHERE ci.name = ?
    """, (city_name,)).fetchone()
    conn.close()
    return dict(row) if row else None


def query_filtered_cities(country=None, min_pop=0, max_pop=10000000, equity_categories=None):
    conn = get_connection()
    if equity_categories is None:
        equity_categories = ['Excellent', 'Good', 'Fair', 'Needs Improvement']

    placeholders = ','.join('?' * len(equity_categories))
    sql = f"""
        SELECT
            ci.id AS city_id,
            ci.name AS city_name,
            c.name AS country,
            ci.population,
            ROUND(ut.tree_percentage, 2) AS tree_pct,
            ROUND(cr.pop_density, 0) AS pop_density,
            ROUND(cr.tree_density, 6) AS tree_density,
            ROUND(cr.pop_to_tree_ratio, 0) AS pop_to_tree_ratio,
            (SELECT COUNT(*) FROM city_rankings) + 1 - cr.rank AS equity_rank,
            CASE
                WHEN cr.pop_to_tree_ratio < 64000 THEN 'Excellent'
                WHEN cr.pop_to_tree_ratio < 142000 THEN 'Good'
                WHEN cr.pop_to_tree_ratio < 250000 THEN 'Fair'
                ELSE 'Needs Improvement'
            END AS equity_category
        FROM cities ci
        JOIN countries c ON c.id = ci.country_id
        JOIN urban_trees ut ON ut.city_id = ci.id
        JOIN city_rankings cr ON cr.city_id = ci.id
        WHERE ci.population BETWEEN ? AND ?
          AND equity_category IN ({placeholders})
    """
    params = [min_pop, max_pop] + equity_categories

    if country:
        sql += " AND c.name = ?"
        params.append(country)

    sql += " ORDER BY equity_rank ASC"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]
