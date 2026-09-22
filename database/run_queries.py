"""
Executes and prints results of analytical SQL queries against the local SQLite database.
Runs with standard library sqlite3 (zero external dependencies required).
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "energy_intelligence.db")


def print_table(cursor, title: str, query: str, limit: int = 15):
    print("\n" + "=" * 85)
    print(f"  {title}")
    print("=" * 85)
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    # Calculate column widths
    col_widths = [len(c) for c in columns]
    for r in rows[:limit]:
        for i, val in enumerate(r):
            col_widths[i] = max(col_widths[i], len(str(val) if val is not None else "NULL"))

    # Format header
    header_str = " | ".join(f"{c:<{col_widths[i]}}" for i, c in enumerate(columns))
    sep_str = "-+-".join("-" * col_widths[i] for i in range(len(columns)))
    print(header_str)
    print(sep_str)

    # Format rows
    for r in rows[:limit]:
        row_str = " | ".join(f"{str(val) if val is not None else 'NULL':<{col_widths[i]}}" for i, val in enumerate(r))
        print(row_str)

    if len(rows) > limit:
        print(f"... [{len(rows) - limit} more rows]")


def main():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}. Please run data_pipeline.py and load_database.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query 1: Top Renewable Producers Rank in 2024
    q1 = """
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
        WHERE f.year = 2024
        GROUP BY f.year, c.name, c.region
    )
    SELECT 
        country_name,
        region,
        renewable_twh,
        total_generation_twh,
        renewable_share_pct,
        RANK() OVER (ORDER BY renewable_share_pct DESC) AS global_rank
    FROM country_clean_share
    ORDER BY global_rank
    LIMIT 12;
    """
    print_table(cursor, "1. Global Renewable Share & Country Rankings (2024)", q1)

    # Query 2: Decarbonization Velocity (gCO2/kWh reduction 2005 vs 2024)
    q2 = """
    WITH carbon_metrics AS (
        SELECT 
            c.name AS country_name,
            c.region,
            f.year,
            ROUND(
                (SUM(f.emissions_mtco2) * 1e6) / NULLIF(SUM(f.generation_twh) * 1e3, 0), 1
            ) AS carbon_intensity_gco2_kwh
        FROM fact_power_generation f
        JOIN dim_country c ON f.country_code = c.code
        WHERE f.year IN (2005, 2024)
        GROUP BY c.name, c.region, f.year
    )
    SELECT 
        country_name,
        region,
        MAX(CASE WHEN year = 2005 THEN carbon_intensity_gco2_kwh END) AS intensity_2005,
        MAX(CASE WHEN year = 2024 THEN carbon_intensity_gco2_kwh END) AS intensity_2024,
        ROUND(
            (MAX(CASE WHEN year = 2024 THEN carbon_intensity_gco2_kwh END) - 
             MAX(CASE WHEN year = 2005 THEN carbon_intensity_gco2_kwh END)) * 100.0 /
            NULLIF(MAX(CASE WHEN year = 2005 THEN carbon_intensity_gco2_kwh END), 0), 1
        ) AS reduction_pct
    FROM carbon_metrics
    GROUP BY country_name, region
    ORDER BY reduction_pct ASC
    LIMIT 10;
    """
    print_table(cursor, "2. Top 10 Fastest Decarbonizing Power Grids (% Drop in Carbon Intensity)", q2)

    # Query 3: When Clean Generation Surpassed Coal Generation
    q3 = """
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
    ORDER BY clean_surpassed_coal_year ASC
    LIMIT 12;
    """
    print_table(cursor, "3. Historical Milestone: Year Clean Power Surpassed Coal Generation", q3)

    conn.close()


if __name__ == "__main__":
    main()
