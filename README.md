# INDIAN-STOCK-MARKET-ANALYSIS
This is a project involving the use of advance SQL, little of Python and Excel. The whole pipeline is automated with python script and tasks, the python script get the data from the websites and then a new script analyses the data on pre-made queries and returns the data into a raw  excel-file; which later goes to the main sheet for visualisation
# 🇮🇳 Indian Stock Market Analysis & Executive Dashboard (1-Year)

A robust, end-to-end data pipeline and executive dashboard project that extracts Indian stock market historical data, processes and transforms it via advanced SQL, and integrates safely with an interactive, professionally styled Excel Executive Dashboard using Power Query.

---

## 🚀 Project Overview
This project solves a common data engineering problem: **the "overwrite trap"**, where automated scripts wipe out manual layouts, charts, and KPI cards. By decoupling the **Data Layer** (Python + SQLite) from the **Presentation Layer** (Excel + Power Query), this project maintains a bulletproof, automated reporting pipeline.

---

## 🏗️ Pipeline Architecture & Workflow

`Yahoo Finance API` ➡️ `Python Script (Extraction)` ➡️ `SQLite Database (indian_stocks.db)` ➡️ `Automated Raw Export (raw_stock_data.xlsx)` ➡️ `Excel Power Query & Data Model` ➡️ `MAIN_EXECUTIVE_DASHBOARD.xlsx`

The project follows a 5-stage automated pipeline:
1. **Data Source:** Pulls 1-year historical pricing, volume, and market metrics for key Indian stocks (`RELIANCE.NS`, `TCS.NS`, `INFY.NS`, `SBIN.NS`, `HDFCBANK.NS`).
2. **Extraction & Storage (Python & SQLite):** Stores raw records in `indian_stocks.db`. Advanced SQL queries leveraging **CTEs (Common Table Expressions)** and **Window Functions (`ROW_NUMBER()`, `LAG()`)** compute daily price jumps, percentage returns, volume spikes, and sector rankings.
3. **Raw Data Export:** Python securely exports query results into a dedicated raw data file (`raw_stock_data.xlsx`) without touching the presentation workbook.
4. **Data Connection & Transformation (Power Query):** Excel ingests `raw_stock_data.xlsx`, handling data typing and cleaning automatically on every refresh.
5. **Executive Dashboard:** A polished, app-like visual report featuring dynamic KPI cards, interactive slicers, custom charts, and dynamic header updates.

---

## 📊 Key Features & Fundamentals
- **Advanced SQL Analytics:** Utilizes CTEs, Window Functions, and multi-table joins to rank companies by percentage return and isolate high-volume trading sessions.
- **Overwrite-Proof Architecture:** Clean structural separation of raw data generation and visual reporting.
- **Dynamic Excel Integration:** Slicers dynamically update charts and KPI metrics across the workbook.
- **Professional Formatting:** Custom color palettes, comma-separated volumes, formatted percentages, and hidden gridlines.

---

## 🎥 Video Demonstration 

### Video Walkthrough
![My Dashboard Demo](https://github.com/Shubhyam-f/INDIAN-STOCK-MARKET-ANALYSIS/blob/main/Stock%20market%20analysis%20video.gif)

---

## 📂 Project Directory Structure
```text
Indian_Stock_Project/
│
├── indian_stocks.db                  # SQLite Database storing raw historical data
├── export_raw_data.py                # Python script for SQL extraction & raw export
├── raw_stock_data.xlsx               # Automated raw data source file (safe to overwrite)
└── MAIN_EXECUTIVE_DASHBOARD.xlsx     # Final executive-level visual dashboard
