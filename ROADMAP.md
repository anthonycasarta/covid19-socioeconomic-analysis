# Roadmap

This roadmap tracks completed work and remaining development for the Databricks COVID-19 socioeconomic analysis project.

## Completed

- Implemented a Databricks Declarative Automation Bundle.
- Added a development bundle target for Databricks Free Edition.
- Added the serverless `project_setup` job.
- Added the serverless `socioeconomic_etl` job.
- Added the serverless `socioeconomic_pipeline`.
- Defined landing tasks for COVID-19, GDP, and healthcare data.
- Added task dependencies so the pipeline runs after all landing tasks complete.
- Added setup logic for the catalog, Bronze, Silver, and Gold schemas, volumes, and source directories.
- Added shared landing utilities for HTTP downloads, ZIP extraction, CSV writing, and healthcare file copying.
- Added six Bronze Streaming Tables.
- Added COVID-19 profiling and null-rate analysis.
- Added `silver.covid_daily` as the initial cleaned COVID-19 Streaming Table.
- Validated and deployed the bundle through the Databricks CLI.

## Current Structure

```text
covid19-socioeconomic-analysis/
├── databricks.yml
├── resources/
│   ├── jobs.yml
│   └── pipelines.yml
├── data/
│   ├── health_centers_density.csv
│   ├── hospital_beds.csv
│   ├── hospital_density.csv
│   ├── hospital_medicine.csv
│   └── README.md
├── landing/
│   ├── covid.py
│   ├── gdp.py
│   ├── healthcare.py
│   └── utils.py
├── notebooks/
│   ├── 00_setup.py
│   └── 02_data_preprocessing_covid.py
├── pipelines/
│   ├── bronze/
│   │   ├── covid_bronze_raw.sql
│   │   ├── gdp_ingestion.sql
│   │   ├── health_centers_density_ingestion.sql
│   │   ├── hospital_beds_ingestion.sql
│   │   ├── hospital_density_ingestion.sql
│   │   └── hospital_medicine_ingestion.sql
│   └── silver/
│       └── covid_silver.sql
├── README.md
└── ROADMAP.md
```

## Next Steps

### COVID-19 Ingestion

1. Detect whether the OWID source changed before saving another snapshot.
2. Prevent multiple complete snapshots from producing duplicate Bronze records.
3. Choose an explicit snapshot replacement or immutable versioning strategy.
4. Preserve the source filename and ingestion timestamp in Bronze.
5. Verify pipeline refresh behavior when the OWID snapshot changes.

### COVID-19 Silver

1. Enable country-code and valid-date filters.
2. Validate `(country_code, observation_date)` uniqueness.
3. Define how duplicate records are resolved.
4. Define how historical reporting corrections are handled.
5. Add required-column checks.
6. Add plausible-range checks for cases, deaths, population, and rates.

### GDP Processing

1. Inspect and document the World Bank Bronze schema.
2. Create a cleaned GDP Silver table.
3. Preserve indicator name, indicator code, source year, and units.
4. Convert year columns into an analysis-friendly row structure.
5. Validate country identifiers and GDP values.

### Healthcare Processing

1. Inspect and document each healthcare Bronze schema.
2. Create Silver transformations for all four healthcare datasets.
3. Preserve reporting year, unit, and indicator dimensions.
4. Standardize column names and data types.
5. Validate country identifiers and indicator values.

### Data Integration

1. Define a canonical country dimension.
2. Standardize ISO country codes across all sources.
3. Define the analysis period.
4. Define the COVID-19 mortality outcome.
5. Decide how daily COVID-19 observations align with annual GDP and healthcare indicators.
6. Build an integrated country-level Gold table.
7. Document the grain and join rules for the integrated dataset.

### Data Quality And Testing

1. Add automated checks for required columns and data types.
2. Add uniqueness checks for expected table grains.
3. Add accepted-value and plausible-range checks.
4. Add tests for landing utility functions.
5. Add pipeline tests using representative sample data.
6. Record rejected or invalid records instead of silently dropping them.

### Bundle Enhancements

1. Add a production bundle target.
2. Parameterize the remaining hard-coded catalog and volume paths in `notebooks/00_setup.py`.
3. Add schedules when recurring ingestion is required.
4. Add job and pipeline permissions.
5. Add bundle validation to CI.
6. Test and document a clean workspace bootstrap.
7. Define environment-specific pipeline settings and source paths.

## Later Work

- Add exploratory analysis and visualizations.
- Compare mortality outcomes with GDP and healthcare capacity.
- Evaluate correlations and potential confounding variables.
- Document assumptions, limitations, and data coverage.
- Add statistical or machine-learning models only after the integrated dataset is stable.
- Add dashboards or reports for the final analysis.
