# Power BI Desktop Integration Guide

This directory contains everything required to load and visualize the **Energy Transition Intelligence Platform** in Microsoft Power BI Desktop.

## Files Included:
1. `master_energy_transition_for_powerbi.csv`: The denormalized clean dataset containing all dimensions and facts.
2. `dax_measures.txt`: Pre-built DAX formulas for instant KPI cards and calculations.

---

## 3-Minute Quick Setup in Power BI Desktop:

1. **Load Data:**
   * Open Power BI Desktop.
   * Click **Get Data** -> **Text/CSV** -> Select `master_energy_transition_for_powerbi.csv`.
   * Click **Load**.

2. **Add DAX Measures:**
   * In the Fields pane, right-click on the table and select **New Measure**.
   * Copy and paste the measures from `dax_measures.txt` (e.g., `Clean_Share_Pct`, `Avg_Solar_LCOE`, `Capacity_YoY_Growth_GW`).

3. **Recommended Visual Layout (3-Page Executive Report):**
   * **Page 1: Executive Market Summary**
     * Top Cards: Total Clean Gen (TWh), Clean Share %, Solar LCOE ($/MWh), Total Emissions (MtCO2).
     * Area Chart: `year` on X-axis, `Total_Generation_TWh` on Y-axis, `category` in Legend.
     * Slicer: `name` (Country selector).
   * **Page 2: Technology & Cost Trajectories**
     * Line Chart: `year` on X-axis, `lcoe_usd_per_mwh` on Y-axis, `name_y` (Technology) in Legend.
     * Bar Chart: Top 10 Countries by `Clean_Share_Pct`.
   * **Page 3: Net-Zero Progress Tracker**
     * Clustered Column Chart: `name` on X-axis, `Grid_Carbon_Intensity` comparing 2005 vs 2024.
