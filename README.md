<div align="center">

# ⚡ Energy Transition Intelligence Platform
### Renewable Asset Growth, Clean Power Modeling & LCOE Cost-Benchmark Engine

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Meta Prophet](https://img.shields.io/badge/Meta-Prophet-0081FB?logo=meta&logoColor=white)](https://facebook.github.io/prophet/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <b>An end-to-end data engineering, statistical forecasting, and executive business intelligence platform analyzing global power decarbonization trajectories across 35+ economies (2005–2024) with projections to 2035.</b>
</p>

[Key Features](#-key-features) •
[Architecture](#-architecture) •
[Data Model (Star Schema)](#-star-schema-data-warehouse) •
[Tech Stack](#-technical-stack) •
[Quickstart](#-quickstart-guide) •
[Power BI Integration](#-power-bi-asset-pack)

---

</div>

## 📌 Executive Overview & Motivation

As the global power sector races toward net-zero, energy intelligence firms (e.g., *Rystad Energy*) require structured, asset-level databases to evaluate the velocity of renewable capacity expansion, Levelized Cost of Electricity (LCOE) deflation, and grid carbon intensity shifts.

This platform automates the multi-country energy transition analysis workflow:
1. **Automated ETL Pipeline:** Ingests and cleans 15+ years of power generation, installed capacity, emissions, and LCOE benchmarks across **35+ countries** (US EIA & Ember Climate benchmarks).
2. **Relational Data Warehouse:** Architected in **PostgreSQL / SQLite** using a normalized **Star Schema** with analytical SQL window functions (`RANK()`, `LAG()`, `LEAD()`) and CTEs.
3. **Forecasting Engine:** Leverages **Meta Prophet** to forecast clean energy installed capacity to **2035**, achieving **~15% lower forecast error (MAPE)** over baseline persistence models.
4. **Dual Client Deliverables:** Interactive executive dashboards delivered via **Streamlit** and pre-built **Microsoft Power BI** DAX models.

---

## ⚡ Key Features

* 📊 **Multi-Country Fuel-Mix Dynamics:** Evaluates historical generation shares (Solar PV, Onshore Wind, Offshore Wind, Hydropower, Nuclear, Natural Gas, Coal) from 2005 to 2024.
* 📉 **LCOE Cost Deflation Tracker:** Traces the ~88% collapse of Solar PV generation costs ($350/MWh in 2005 to under $40/MWh in 2024) and onshore wind grid-parity dynamics.
* 🔮 **2035 Net-Zero Capacity Horizon:** Projects future capacity additions with 95% confidence intervals, benchmarking 2030 targets (9,986 GW projected).
* 🗄️ **Star Schema & Live SQL Analytics:** Built-in SQL explorer executing real-time window functions to rank nations by decarbonization velocity.
* 📈 **Executive Power BI Pack:** Includes pre-calculated DAX formulas (`Clean_Share_Pct`, `LCOE_Trend`, `YoY_Growth`) and clean CSVs for instant corporate presentation.

---

## 🏗️ Architecture

```
[Raw Sources: US EIA REST API / Ember Climate / IRENA LCOE]
                           │
                           ▼
          [Python Automated ETL & Quality Validator]
      (Missing-data interpolation, unit standardization TWh/GW)
                           │
                           ▼
     [Relational Star-Schema Data Warehouse (PostgreSQL / SQLite)]
     ├── Dim_Country    (35+ Major Economies, Income, Net-Zero Targets)
     ├── Dim_Technology (Solar, Wind, Hydro, Nuclear, Gas, Coal)
     ├── Dim_Time       (2000-2039 Decades & Policy Eras)
     └── Fact_PowerGen  (Generation TWh, Capacity GW, Emissions, LCOE)
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
    [Meta Prophet Forecast]    [Executive Deliverables]
    ├── 2025-2035 Horizon      ├── Streamlit Live Web App
    ├── Baseline Persistence   └── Power BI Desktop Asset Pack
    └── ~15% Lower MAPE            (DAX Measures & Star Schema)
```

---

## 🗄️ Star-Schema Data Warehouse

The database is modeled into an optimized Star Schema supporting sub-second analytical aggregations:

```
                  ┌────────────────────────┐
                  │      Dim_Country       │
                  ├────────────────────────┤
                  │ PK  code (VARCHAR)     │
                  │     name               │
                  │     region             │
                  │     income             │
                  │     net_zero_target    │
                  └───────────┬────────────┘
                              │ 1
                              │
                              │ *
┌──────────────────────┐  ┌───┴────────────────────────┐  ┌──────────────────────┐
│    Dim_Technology    │  │  Fact_PowerGeneration      │  │       Dim_Time       │
├──────────────────────┤  ├────────────────────────────┤  ├──────────────────────┤
│ PK  tech_id (INT)    ├──┤ FK  country_code           ├──┤ PK  year (INT)       │
│     name             │1*│ FK  tech_id                │*1│     decade           │
│     category         │  │ FK  year                   │  │     policy_era       │
│     emission_factor  │  │     generation_twh         │  └──────────────────────┘
└──────────────────────┘  │     capacity_gw            │
                          │     emissions_mtco2        │
                          │     lcoe_usd_per_mwh       │
                          └────────────────────────────┘
```

---

## 💻 Technical Stack

| Domain | Technology / Library | Purpose in Project |
| :--- | :--- | :--- |
| **Data Engineering** | `Python 3.10+`, `pandas`, `requests` | API extraction, data cleansing, unit conversion |
| **Data Warehousing** | `PostgreSQL 16`, `SQLite 3`, `SQLAlchemy` | Star-schema storage, DDL constraints, indexing |
| **Advanced SQL** | `Window Functions`, `CTEs`, `HAVING` | YoY growth (`LAG`), country rankings (`RANK`) |
| **Forecasting** | `Meta Prophet`, `Scikit-learn`, `numpy` | 2035 capacity trajectory, MAPE benchmark |
| **Visualization** | `Streamlit`, `Plotly Express`, `Plotly Graph Objects` | Interactive web dashboard, stacked area charts |
| **Enterprise BI** | `Microsoft Power BI Desktop`, `DAX` | Client-facing executive report pack |

---

## 📊 Model Validation Benchmark

The forecasting engine evaluates performance against a held-out test period (2020–2024):

| Model Architecture | Evaluation Horizon | Test MAPE | Result |
| :--- | :---: | :---: | :---: |
| **Naive Persistence Drift Baseline** | 2020 – 2024 | `10.84%` | Benchmark baseline |
| **Meta Prophet Multivariate Model** | 2020 – 2024 | **`5.49%`** | **~49.4% lower error (~15% target met)** |

* **2030 Clean Installed Capacity Target:** Projected to reach **`9,986 GW`** globally.
* **2035 Clean Installed Capacity Target:** Projected to reach **`13,917 GW`** globally.

---

## 🚀 Quickstart Guide

### 1. Clone & Setup Environment
```bash
git clone https://github.com/ShivaliGupta17/Energy-Transition-Intelligence-Renewable-Asset-Clean-Power-Platform-.git
cd Energy-Transition-Intelligence-Renewable-Asset-Clean-Power-Platform-
pip install -r requirements.txt
```

### 2. Execute Data Pipeline & Initialize Database
```bash
# Run automated ETL (downloads, cleans & validates data)
python data_pipeline.py

# Initialize Star Schema in SQLite & load tables
python database/load_database.py

# Execute advanced analytical SQL queries (window functions & rankings)
python database/run_queries.py
```

### 3. Run Prophet Forecasting Engine
```bash
python forecasting/prophet_forecast.py
```

### 4. Launch Executive Dashboard
```bash
python -m streamlit run dashboard/app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 📈 Power BI Asset Pack

For corporate presentations in Power BI Desktop:
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV** -> Select [`dashboard/powerbi/master_energy_transition_for_powerbi.csv`](dashboard/powerbi/master_energy_transition_for_powerbi.csv).
3. Copy-paste the pre-calculated DAX formulas from [`dashboard/powerbi/dax_measures.txt`](dashboard/powerbi/dax_measures.txt):
   * `Clean_Share_Pct`
   * `Capacity_YoY_Growth_GW`
   * `Avg_Solar_LCOE`
   * `Grid_Carbon_Intensity`
4. Follow the layout instructions in [`dashboard/powerbi/README_PBI.md`](dashboard/powerbi/README_PBI.md).

---

## 👤 Author

**Shivali Gupta**  
*M.Sc. Data Science, Indian Institute of Information Technology, Lucknow (GPA: 9.15)*    
* [LinkedIn](https://www.linkedin.com/in/shivali-gupta07/) • [GitHub](https://github.com/ShivaliGupta17) • Email: [shivaligpt17@gmail.com](mailto:shivaligpt17@gmail.com)
