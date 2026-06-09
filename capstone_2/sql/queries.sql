-- ============================================================
-- Capstone 2: Data Modeling — SQL Queries
-- European Urban Tree Cover Analysis
-- ============================================================
-- 5 queries: 2 Easy, 2 Medium, 1 Difficult
-- ============================================================

-- ============================================================
-- EASY QUERY 1: Cities per Country with Average Population
-- Tables: cities, countries
-- Features: JOIN, GROUP BY, COUNT, AVG, ORDER BY
-- ============================================================

SELECT
    c.name AS country_name,
    COUNT(ci.id) AS city_count,
    AVG(ci.population) AS avg_city_population
FROM countries c
JOIN cities ci ON ci.country_id = c.id
GROUP BY c.name
ORDER BY city_count DESC, avg_city_population DESC;


-- ============================================================
-- EASY QUERY 2: Cities with Above-Average Tree Cover
-- Tables: cities, urban_trees
-- Features: JOIN, WHERE, ORDER BY, ROUND
-- ============================================================

SELECT
    ci.name AS city_name,
    ROUND(ut.tree_percentage, 2) AS tree_pct,
    ROUND(ut.tree_cover_km2, 2) AS tree_km2
FROM cities ci
JOIN urban_trees ut ON ut.city_id = ci.id
WHERE ut.tree_percentage > 2.0
ORDER BY ut.tree_percentage DESC;


-- ============================================================
-- MEDIUM QUERY 1: Top 10 Cities by Tree Equity Ranking
-- Tables: cities, countries, urban_trees, city_rankings
-- Features: 4-table JOIN, TOP-N, string function (SUBSTR),
--           WHERE (tree_pct threshold), ORDER BY, LIMIT
-- ============================================================

SELECT
    ci.name AS city_name,
    SUBSTR(c.name, 1, 3) AS country_code,
    ROUND(ut.tree_percentage, 2) AS tree_pct,
    ROUND(cr.pop_density, 0) AS pop_density,
    cr.rank AS equity_rank
FROM cities ci
JOIN countries c ON c.id = ci.country_id
JOIN urban_trees ut ON ut.city_id = ci.id
JOIN city_rankings cr ON cr.city_id = ci.id
WHERE ut.tree_percentage > 1.0
ORDER BY cr.rank ASC
LIMIT 10;


-- ============================================================
-- MEDIUM QUERY 2: National Population Context for Cities
-- Tables: countries, population_annual, cities
-- Features: 3-table JOIN, WHERE (year = 2025),
--           string function (SUBSTR), GROUP BY, ORDER BY
-- ============================================================

SELECT
    c.name AS country_name,
    SUBSTR(c.iso_code, 1, 2) AS iso,
    COUNT(ci.id) AS cities_in_dataset,
    pa.population_count AS national_pop_2025,
    ROUND(pa.population_count / COUNT(ci.id), 0) AS pop_per_city_ratio
FROM countries c
JOIN population_annual pa ON pa.country_id = c.id
JOIN cities ci ON ci.country_id = c.id
WHERE pa.year = 2025
GROUP BY c.name
ORDER BY national_pop_2025 DESC;


-- ============================================================
-- DIFFICULT QUERY: Multi-Factor City Tree Equity Analysis
-- Tables: cities, countries, urban_trees, city_rankings
-- Features: 4-table JOIN, nested subquery, WHERE filtering,
--           CASE expression, string function, date function,
--           aggregation, ORDER BY

SELECT
    ci.name AS city_name,
    SUBSTR(ci.name, 1, 4) AS short_name,
    c.name AS country,
    ROUND(ut.tree_percentage, 2) AS tree_pct,
    ROUND(cr.pop_density, 0) AS pop_per_km2,
    ROUND(cr.pop_to_tree_ratio, 0) AS people_per_tree_km2,
    cr.rank AS equity_rank,
    CAST(strftime('%Y', 'now') AS INTEGER) - ut.source_year AS years_since_measured,
    CASE
        WHEN cr.rank <= 5 THEN 'Excellent'
        WHEN cr.rank <= 15 THEN 'Good'
        ELSE 'Needs Improvement'
    END AS equity_category,
    ut.source_year AS measurement_year
FROM cities ci
JOIN countries c ON c.id = ci.country_id
JOIN urban_trees ut ON ut.city_id = ci.id
JOIN city_rankings cr ON cr.city_id = ci.id
WHERE ci.population > 500000
  AND cr.pop_to_tree_ratio < (
    SELECT AVG(cr2.pop_to_tree_ratio)
    FROM city_rankings cr2
  )
ORDER BY cr.rank ASC;
