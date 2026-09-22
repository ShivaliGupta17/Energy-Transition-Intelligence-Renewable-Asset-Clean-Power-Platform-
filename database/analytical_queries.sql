-- ====================================================================
-- Energy Transition Intelligence: Advanced Analytical SQL Queries
-- Demonstrating Window Functions, CTEs, Aggregations, and Market Benchmarking
-- ====================================================================

-- 1. Year-over-Year (YoY) Renewable Capacity Growth Rate using LAG() Window Function
WITH renewable_yearly AS (
    SELECT 
        c.name AS country_name,
        f.year,
        ROUND(SUM(f.capacity_gw), 2) AS total_renewable_capacity_gw
    FROM fact_power_generation f
    JOIN dim_country c ON f.country_code = c.code
    JOIN dim_technology t ON f.tech_id = t.tech_id
    WHERE t.category = 'Renewable'
    GROUP BY c.name, f.year
)
SELECT 
    country_name,
    year,
    total_renewable_capacity_gw,
    LAG(total_renewable_capacity_gw, 1) OVER (
        PARTITION BY country_name ORDER BY year
    ) AS prev_year_capacity_gw,
    ROUND(
        (total_renewable_capacity_gw - LAG(total_renewable_capacity_gw, 1) OVER (
            PARTITION BY country_name ORDER BY year
        )) / NULLIF(LAG(total_renewable_capacity_gw, 1) OVER (
            PARTITION BY country_name ORDER BY year
        ), 0) * 100, 2
    ) AS yoy_growth_pct
FROM renewable_yearly
WHERE year >= 2015
ORDER BY country_name, year;


-- 2. Ranking Top Renewable Power Producers per Year using RANK() Window Function
WITH country_clean_share AS (
    SELECT 
        f.year,
        c.name AS country_name,
        c.region,
        ROUND(SUM(CASE WHEN t.category = 'Renewable' THEN f.generation_twh ELSE 0 END), 2) AS renewable_twh,
        ROUND(SUM(f.generation_twh), 2) AS total_generation_twh,
        ROUND(
            SUM(CASE WHEN t.category = 'Renewable' THEN f.generation_twh ELSE 0 END) * 100.0 / NULLIF(SUM(f.generation_twh), 0), 2
        ) AS renewable_share_pct
    FROM fact_power_generation f
    JOIN dim_country c ON f.country_code = c.code
    JOIN dim_technology t ON f.tech_id = t.tech_id
    GROUP BY f.year, c.name, c.region
)
SELECT 
    year,
    country_name,
    region,
    renewable_twh,
    renewable_share_pct,
    RANK() OVER (
        PARTITION BY year ORDER BY renewable_share_pct DESC
    ) AS global_renewable_rank
FROM country_clean_share
WHERE year IN (2010, 2015, 2020, 2024)
ORDER BY year, global_renewable_rank;


-- 3. Decarbonization Velocity & Grid Carbon Intensity (gCO2 / kWh) from 2005 to 2024
WITH carbon_metrics AS (
    SELECT 
        c.name AS country_name,
        c.income,
        f.year,
        ROUND(SUM(f.emissions_mtco2), 2) AS total_emissions_mtco2,
        ROUND(SUM(f.generation_twh), 2) AS total_generation_twh,
        ROUND(
            (SUM(f.emissions_mtco2) * 1e6) / NULLIF(SUM(f.generation_twh) * 1e3, 0), 1
        ) AS carbon_intensity_gco2_kwh
    FROM fact_power_generation f
    JOIN dim_country c ON f.country_code = c.code
    GROUP BY c.name, c.income, f.year
)
SELECT 
    country_name,
    income,
    MAX(CASE WHEN year = 2005 THEN carbon_intensity_gco2_kwh END) AS intensity_2005,
    MAX(CASE WHEN year = 2024 THEN carbon_intensity_gco2_kwh END) AS intensity_2024,
    ROUND(
        MAX(CASE WHEN year = 2024 THEN carbon_intensity_gco2_kwh END) - 
        MAX(CASE WHEN year = 2005 THEN carbon_intensity_gco2_kwh END), 1
    ) AS absolute_reduction_gco2_kwh,
    ROUND(
        (MAX(CASE WHEN year = 2024 THEN carbon_intensity_gco2_kwh END) - 
         MAX(CASE WHEN year = 2005 THEN carbon_intensity_gco2_kwh END)) * 100.0 /
        NULLIF(MAX(CASE WHEN year = 2005 THEN carbon_intensity_gco2_kwh END), 0), 1
    ) AS reduction_pct
FROM carbon_metrics
GROUP BY country_name, income
ORDER BY reduction_pct ASC;


-- 4. Fuel-Mix Flip Point: The Historical Year Clean Generation Surpassed Coal Generation
WITH clean_vs_coal AS (
    SELECT 
        c.name AS country_name,
        f.year,
        SUM(CASE WHEN t.category IN ('Renewable', 'Low-Carbon') THEN f.generation_twh ELSE 0 END) AS clean_twh,
        SUM(CASE WHEN t.name = 'Coal' THEN f.generation_twh ELSE 0 END) AS coal_twh
    FROM fact_power_generation f
    JOIN dim_country c ON f.country_code = c.code
    JOIN dim_technology t ON f.tech_id = t.tech_id
    GROUP BY c.name, f.year
)
SELECT 
    country_name,
    MIN(year) AS clean_surpassed_coal_year
FROM clean_vs_coal
WHERE clean_twh > coal_twh
GROUP BY country_name
ORDER BY clean_surpassed_coal_year ASC;
