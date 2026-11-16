# ⚽ Premier League Data Engineering Lakehouse

**End-to-End Data Engineering Pipeline | Databricks · PySpark · Delta Lake · SQL · Python**

An end-to-end data engineering project that ingests Premier League football data from a REST API, transforms it through a Medallion Architecture using PySpark and Delta Lake, and delivers analytics-ready datasets to an interactive Databricks AI/BI dashboard.

The project demonstrates API ingestion, data transformation, Delta Lake storage, workflow orchestration, data quality validation and analytical reporting.

## 📊 Dashboard

The final output is a Premier League analytics dashboard built using Databricks AI/BI.

![Premier League Analytics Dashboard](dashboard/PL%20Dashboard.png)

The dashboard includes:

- **Season KPIs:** Total teams, completed matches and total goals.
- **League standings:** Team positions, results, goals and points.
- **Top 10 teams:** Ranking by league points.
- **Top 10 goalscorers:** Player goalscoring statistics.

The dashboard queries Gold-layer Delta tables and Silver match data using SQL.

[View dashboard definition](dashboard/Premier%20League%20Analytics%20-%202026-27.lvdash.json)

## 🏗️ Data Architecture

The pipeline follows the **Medallion Architecture**, separating raw, cleaned and analytics-ready data.

```text
football-data.org REST API
           |
           v
    Python API Extraction
           |
           v
  Databricks Unity Catalog Volume
       (Raw JSON Files)
           |
           v
    BRONZE LAYER
    Raw Delta Tables
           |
           v
    SILVER LAYER
    Cleaned & Structured Data
           |
           v
     GOLD LAYER
     Analytics-Ready Tables
           |
           v
    Databricks AI/BI Dashboard
```

### Bronze Layer — Raw Data

Raw API responses are ingested into Delta Lake tables.

Datasets include:

- Teams
- Matches
- Standings
- Goalscorers
- Competition metadata

### Silver Layer — Cleaned Data

PySpark transformations convert nested API responses into structured datasets.

The Silver layer prepares consistent columns and data types for downstream analytics.

### Gold Layer — Business Analytics

The Gold layer produces analytics-ready datasets for:

- Premier League standings
- Team performance
- Player statistics
- League summary metrics

These tables support SQL analysis and dashboard visualisations.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | REST API extraction |
| football-data.org API | Premier League data source |
| Azure Databricks | Data processing and orchestration environment |
| PySpark | Distributed data transformations |
| Delta Lake | Lakehouse table storage |
| SQL | Data querying and analytics |
| Unity Catalog | Data organisation and governance |
| Databricks Workflows | Pipeline orchestration |
| Databricks AI/BI | Dashboard and reporting |
| Git & GitHub | Version control and portfolio documentation |

## 🔄 Pipeline Orchestration

The pipeline uses Databricks Workflows to coordinate data processing tasks.

The workflow includes:

1. Bronze data ingestion.
2. Silver transformations for five football datasets.
3. Gold-layer analytical transformations.
4. Cross-table data validation.

Task dependencies control execution order, allowing independent transformations to run in parallel where configured.

## ✅ Data Quality Validation

A dedicated validation notebook performs cross-table consistency checks.

The validation stage is designed to help identify data integrity issues before the datasets are used for analytics.

See [`11_cross_table_validation.ipynb`](databricks/validation/11_cross_table_validation.ipynb).

## 📁 Repository Structure

```text
premier-league-data-engineering/
├── src/
│   └── extract.py
├── data/
│   └── raw/                 # Local raw data (Git ignored)
├── databricks/
│   ├── extraction/
│   │   └── 00_api_extraction.ipynb
│   ├── bronze/
│   │   └── 01_bronze_ingestion.ipynb
│   ├── silver/
│   │   ├── 02_silver_teams.ipynb
│   │   ├── 03_silver_matches.ipynb
│   │   ├── 04_silver_standings.ipynb
│   │   ├── 05_silver_scorers.ipynb
│   │   └── 06_silver_competition.ipynb
│   ├── gold/
│   │   ├── 07_gold_league_table.ipynb
│   │   ├── 08_gold_team_performance.ipynb
│   │   ├── 09_gold_player_stats2.ipynb
│   │   └── 10_gold_league_summary.ipynb
│   └── validation/
│       └── 11_cross_table_validation.ipynb
├── dashboard/
│   ├── PL Dashboard.png
│   └── Premier