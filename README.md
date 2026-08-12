# COVID-19 Socioeconomic Analysis

A Databricks project for analyzing relationships between COVID-19 mortality, economic conditions, and healthcare capacity across countries.

> **Status:** Bronze ingestion and initial COVID-19 Silver preprocessing are implemented. The socioeconomic analysis is not yet complete.

## Current Functionality

The project currently:

- Ingests COVID-19 data from Our World in Data.
- Ingests GDP-per-capita data from the World Bank.
- Loads healthcare indicator CSV files from `data/`.
- Creates Bronze streaming tables for each source.
- Profiles COVID-19 record counts and null rates.
- Creates the `silver.covid_daily` streaming table.

The COVID-19 Silver table:

- Uses country and observation date as its intended grain.
- Standardizes country and date columns.
- Casts measures to appropriate data types.
- Retains raw, smoothed, cumulative, and per-million measures.
- Preserves missing values and negative reporting corrections.
- Flags negative case and death corrections.

## Repository Structure

```text
covid19-socioeconomic-analysis/
├── data/
│   ├── health_centers_density.csv
│   ├── hospital_beds.csv
│   ├── hospital_density.csv
│   └── hospital_medicine.csv
├── notebooks/
│   ├── 01_data_ingestion.py
│   └── 02_data_preprocessing_covid.py
├── README.md
└── ROADMAP.md
```

## Data Sources

- Our World in Data COVID-19 dataset
- World Bank GDP-per-capita dataset
- Healthcare indicator CSV files under `data/`

## Data Pipeline

```text
COVID-19 CSV
    |
    v
bronze.covid_owid_raw
    |
    v
silver.covid_daily

GDP ZIP
    |
    v
bronze.gdp_world_bank_raw

Healthcare CSVs
    |
    v
Bronze healthcare streaming tables
```

## Running the Project

The project requires a Databricks workspace with Unity Catalog access and support for streaming tables.

Run the notebooks in this order:

1. `notebooks/01_data_ingestion.py`
2. `notebooks/02_data_preprocessing_covid.py`

The preprocessing notebook currently invokes the ingestion notebook using `%run`.

Verify the COVID-19 Silver table:

```sql
SELECT COUNT(*) AS record_count
FROM covid19_socioeconomic_analysis.silver.covid_daily;
```

## Known Limitations

- Country-date uniqueness is not enforced.
- Duplicate country-date records are not handled.
- Country-code and valid-date filters are commented out.
- The COVID-19 source can change between runs.
- GDP and healthcare Silver preprocessing are not implemented.
- The datasets have not been joined or analyzed.
- There is no automated test suite.

See `ROADMAP.md` for planned work.
