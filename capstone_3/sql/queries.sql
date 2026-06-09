-- ============================================================
-- Capstone 3: Dashboard Development — SQL Queries
-- European Urban Tree Cover Analysis
-- Optimized for dashboard data retrieval
-- ============================================================

-- ============================================================
-- QUERY 1: All Cities with Full Metrics
-- Used by: Both dashboards — map, tables, all charts
-- Tables: cities, countries, urban_trees, city_rankings
-- Features: 4-table JOIN, ROUND, CASE equity category
-- ============================================================

SELECT
    ci.id AS city_id,
    ci.name AS city_name,
    c.name AS country,
    c.iso_code,
    ci.population,
    ci.urban_area_km2,
    ci.lat,
    ci.lon,
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
    END AS equity_category
FROM cities ci
JOIN countries c ON c.id = ci.country_id
JOIN urban_trees ut ON ut.city_id = ci.id
JOIN city_rankings cr ON cr.city_id = ci.id
WHERE ci.lat IS NOT NULL AND ci.lon IS NOT NULL
ORDER BY equity_rank ASC;


-- ============================================================
-- QUERY 2: Top 10 Cities by Tree Cover Percentage
-- Used by: Dashboard 1 — bar chart
-- ============================================================

SELECT
    ci.name AS city_name,
    c.name AS country,
    ROUND(ut.tree_percentage, 2) AS tree_pct
FROM cities ci
JOIN countries c ON c.id = ci.country_id
JOIN urban_trees ut ON ut.city_id = ci.id
ORDER BY ut.tree_percentage DESC
LIMIT 10;


-- ============================================================
-- QUERY 3: Equity Category Distribution
-- Used by: Dashboard 1 — donut chart
-- ============================================================

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
ORDER BY MIN(cr.pop_to_tree_ratio) ASC;


-- ============================================================
-- QUERY 4: Unique Countries with Cities in Dataset
-- Used by: Dashboard 1 — country filter dropdown
-- ============================================================

SELECT DISTINCT
    c.name AS country_name,
    c.iso_code
FROM countries c
JOIN cities ci ON ci.country_id = c.id
ORDER BY c.name;


-- ============================================================
-- QUERY 5: Filtered Cities by Country
-- Used by: Dashboard 1 — when country filter is applied
-- Parameters: country_name (optional filter)
-- ============================================================

SELECT
    ci.id AS city_id,
    ci.name AS city_name,
    c.name AS country,
    ci.population,
    ROUND(ut.tree_percentage, 2) AS tree_pct,
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
WHERE (? IS NULL OR c.name = ?)
ORDER BY equity_rank ASC;


-- ============================================================
-- QUERY 6: Single City Detail
-- Used by: Dashboard 2 — KPI cards
-- Parameters: city_name
-- ============================================================

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
WHERE ci.name = ?;


-- ============================================================
-- QUERY 7: Cities Filtered by Population Range and Equity
-- Used by: Dashboard 2 — filtered table and charts
-- Parameters: min_pop, max_pop, equity_categories (IN list)
-- ============================================================

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
  AND equity_category IN (?)
ORDER BY equity_rank ASC;
