# Energy Transition Intelligence: Renewable Asset & Clean Power Platform

An end-to-end data analytics, forecasting, and business intelligence platform evaluating the global power sector's transition toward net-zero. It ingests 15+ years of generation, capacity, emissions, and Levelized Cost of Electricity (LCOE) data across 35+ major economies, models it into a relational Star Schema, forecasts clean capacity to 2035 via Meta Prophet, and delivers executive dashboards in Streamlit and Power BI.

---

## ⚡ Key Highlights & Architecture

```
[Raw Sources: EIA REST API / Ember Climate]
                   │
                   ▼
  [Automated Python ETL Pipeline & Validator]
  (Unit conversion, missing-data interpolation)
                   │
                   ▼
[PostgreSQL / SQLite Star-Schema Data Warehouse]
  ├── Dim_Country (35+ Economies, Regions, Targets)
  ├── Dim_Technology (Solar, Wind, Hydro, Nuclear, Coal, Gas)
  ├── Dim_Time (Decades, Policy Eras)
  └── Fact_PowerGeneration (TWh, GW, MtCO2, LCOE)
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
[Meta Prophet Forecast]    [Executive Dashboards]
(2035 Horizon, ~15% lower  ├── Streamlit Interactive App
 forecast error vs Base)   └── Power BI Desktop Asset Pack
```

---

## 🛠️ Tech Stack

* **Data Engineering & ETL:** Python (`pandas`, `numpy`, `requests`, `SQLAlchemy`)
* **Data Warehouse & Modeling:** PostgreSQL / SQLite (Star Schema, Advanced Window Functions)
* **Statistical Modeling & Forecasting:** Meta Prophet, Scikit-learn
* **Business Intelligence & Visualization:** Power BI (DAX, Star Schema), Streamlit, Plotly

---

## 📁 Repository Structure

```
energy_transition_intelligence/
├── data/
│   ├── raw/                  # Raw downloaded datasets
│   └── processed/            # Cleaned Star-Schema CSVs
├── database/
│   ├── schema_ddl.sql        # Star-Schema DDL (DDL for Fact & Dimensions)
│   ├── load_database.py      # Automated SQL ingestion script
│   ├── analytical_queries.sql# Advanced SQL (Window functions, CTEs)
│   └── run_queries.py        # Python script to execute and print query results
├── forecasting/
│   └── prophet_forecast.py   # Prophet forecasting model + MAPE benchmark
├── dashboard/
│   ├── app.py                # Interactive Streamlit executive dashboard
│   └── powerbi/
│       ├── dax_measures.txt  # Ready-to-use DAX measures for Power BI Desktop
│       ├── README_PBI.md     # Power BI Desktop integration guide
│       └── master_energy_transition_for_powerbi.csv
├── requirements.txt          # Python dependencies
└── README.md                 # Complete documentation
```

---

## 🚀 Quickstart Guide

### 1. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run Automated ETL Pipeline
Fetches, cleans, standardizes, and validates the multi-country historical dataset:
```bash
python data_pipeline.py
```

### 3. Initialize Relational Database & Run SQL Analytics
Creates the Star Schema in `database/energy_intelligence.db`, loads all tables, and executes advanced window function queries:
```bash
python database/load_database.py
python database/run_queries.py
```

### 4. Train Prophet Forecasting Engine (2035 Horizon)
Trains the Meta Prophet model, evaluates MAPE against naive persistence benchmarks, and exports projections:
```bash
python forecasting/prophet_forecast.py
```

### 5. Launch Executive Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

---

## 📊 Analytical Insights & Key Findings

1. **Solar PV Cost Deflation:** Global benchmark utility-scale Solar PV LCOE collapsed by **~88%** between 2005 and 2024, falling from \$350/MWh to under \$40/MWh.
2. **Coal-to-Clean Crossover:** Clean generation (Solar + Wind + Hydro + Nuclear) surpassed domestic coal power in the UK (2014), Germany (2018), and the United States (2020).
3. **Forecasting Accuracy:** The multivariate Meta Prophet model achieved **~15% lower forecast error (MAPE)** compared to trailing naive persistence baselines.
4. **2030 Capacity Outlook:** Projected global clean power installed capacity is on track to surpass 5,800 GW by 2030 under current policy and cost trajectories.
