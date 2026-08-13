# Roadmap

This roadmap tracks the next steps for the Databricks COVID-19 socioeconomic analysis project.

## Completed

- Bronze ingestion now writes streaming tables for the source datasets.
- COVID-19 profiling and null-rate analysis are implemented.
- `silver.covid_daily` exists as a cleaned COVID-19 streaming table.

## Current Structure

```text
covid19-socioeconomic-analysis/
├── data/
│   ├── health_centers_density.csv
│   ├── hospital_beds.csv
│   ├── hospital_density.csv
│   └── hospital_medicine.csv
├── landing/
│   ├── covid.py
│   ├── gdp.py
│   └── healthcare.py
├── pipelines/
│   ├── bronze/
│   │   ├── covid_bronze_raw.sql
│   │   ├── gdp_bronze_raw.sql
│   │   └── healthcare_bronze_raw.sql
│   └── silver/
│       ├── covid_silver.sql
│       ├── gdp_silver.sql
│       └── healthcare_silver.sql
├── notebooks/
│   ├── setup.py
│   └── data_quality/
│       └── covid_profile.py
├── scripts/
│   └── __init__.py
├── README.md
└── ROADMAP.md
```

## Next Steps

### Pipeline Organization

1. Move catalog, schema, and volume creation into `notebooks/setup.py`.
2. Move COVID-19 downloading into `landing/covid.py`.
3. Move GDP downloading and ZIP extraction into `landing/gdp.py`.
4. Move healthcare file copying into `landing/healthcare.py`.
5. Remove duplicate table definitions from the old ingestion and preprocessing notebooks.
6. Keep only declarative table definitions under `pipelines/`.

### COVID-19 Processing

1. Detect whether the OWID source changed before saving another file.
2. Save changed source data using immutable batch names.
3. Preserve source filename and ingestion metadata in Bronze.
4. Enable country-code and valid-date filters in Silver.
5. Validate `(country_code, observation_date)` uniqueness.
6. Define how historical reporting corrections and duplicate records are handled.
7. Add required-column and plausible-range checks.
8. Verify pipeline refresh behavior when the source snapshot changes.

### Remaining Data

1. Create GDP Bronze and Silver pipeline definitions.
2. Create healthcare Bronze and Silver pipeline definitions.
3. Standardize country identifiers across all sources.
4. Preserve source years, units, and reporting dimensions.
5. Define how daily COVID-19 data aligns with annual indicators.

## Databricks Asset Bundle

Implement the Databricks Asset Bundle after the landing and pipeline code is stable so jobs and pipeline configuration are version-controlled in Git.

Planned structure:

```text
covid19-socioeconomic-analysis/
├── databricks.yml
├── resources/
│   ├── jobs.yml
│   └── pipelines.yml
├── src/
│   ├── landing/
│   │   ├── covid.py
│   │   ├── gdp.py
│   │   └── healthcare.py
│   └── pipelines/
│       ├── bronze/
│       │   ├── covid_bronze_raw.sql
│       │   ├── gdp_bronze_raw.sql
│       │   └── healthcare_bronze_raw.sql
│       └── silver/
│           ├── covid_silver.sql
│           ├── gdp_silver.sql
│           └── healthcare_silver.sql
├── notebooks/
│   └── data_quality/
├── tests/
├── README.md
└── ROADMAP.md
```

The Asset Bundle should define:

- A setup task
- Source-file landing tasks
- The Lakeflow pipeline
- Task dependencies
- Pipeline parameters
- Compute configuration
- Development and production targets
- Schedules and permissions

## Later Work

- Build an integrated country-level analysis dataset.
- Define the COVID-19 mortality outcome and analysis period.
- Add exploratory analysis and visualizations.
- Add automated pipeline and data-quality tests.
- Consider aggregated telemetry only if it supports a specific analysis question.
- Add statistical or machine-learning models only after the integrated dataset is stable.
