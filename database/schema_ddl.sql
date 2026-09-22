-- ====================================================================
-- Energy Transition Intelligence: Star-Schema DDL
-- Compatible with PostgreSQL and SQLite
-- ====================================================================

-- 1. Country Dimension
CREATE TABLE IF NOT EXISTS dim_country (
    code VARCHAR(3) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(50) NOT NULL,
    income VARCHAR(50) NOT NULL,
    net_zero_target INT
);

-- 2. Technology Dimension
CREATE TABLE IF NOT EXISTS dim_technology (
    tech_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    emission_factor_gco2_kwh INT NOT NULL
);

-- 3. Time Dimension
CREATE TABLE IF NOT EXISTS dim_time (
    year INT PRIMARY KEY,
    decade VARCHAR(10) NOT NULL,
    policy_era VARCHAR(50) NOT NULL
);

-- 4. Power Generation Fact Table
CREATE TABLE IF NOT EXISTS fact_power_generation (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- or SERIAL in PostgreSQL
    country_code VARCHAR(3) NOT NULL,
    tech_id INT NOT NULL,
    year INT NOT NULL,
    generation_twh DECIMAL(10, 3) NOT NULL,
    capacity_gw DECIMAL(10, 2) NOT NULL,
    emissions_mtco2 DECIMAL(10, 3) NOT NULL,
    lcoe_usd_per_mwh DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (country_code) REFERENCES dim_country(code),
    FOREIGN KEY (tech_id) REFERENCES dim_technology(tech_id),
    FOREIGN KEY (year) REFERENCES dim_time(year)
);

-- Performance Optimization Indexes
CREATE INDEX IF NOT EXISTS idx_fact_country_year ON fact_power_generation (country_code, year);
CREATE INDEX IF NOT EXISTS idx_fact_tech_year ON fact_power_generation (tech_id, year);
CREATE INDEX IF NOT EXISTS idx_fact_year ON fact_power_generation (year);
