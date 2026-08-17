````markdown
# COVID-19 Socioeconomic Analysis

A Databricks Lakehouse project for analyzing relationships between COVID-19 mortality, economic conditions, and healthcare capacity across countries.

> **Status:** Bronze ingestion and COVID-19 Silver preprocessing are implemented. GDP and healthcare Silver transformations and the final socioeconomic analysis are not yet complete.

## Architecture

The project uses:

- Databricks Declarative Automation Bundles
- Serverless Lakeflow Jobs
- Lakeflow Spark Declarative Pipelines
- Auto Loader
- Unity Catalog
- Bronze and Silver Streaming Tables
- PySpark and Spark SQL

```text
project_setup
└── Create catalog, schemas, volumes, and source directories

socioeconomic_etl
├── Land COVID-19 data
├── Land GDP data
├── Copy healthcare data
└── Run socioeconomic_pipeline
    ├── Create or update six Bronze Streaming Tables
    └── Create or update silver.covid_daily
```

## Data Sources

- Our World in Data COVID-19 dataset
- World Bank GDP-per-capita dataset
- Four healthcare indicator CSV files under `data/`

## Repository Structure

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
│   └── hospital_medicine.csv
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

## Output Tables

The pipeline creates these Bronze Streaming Tables:

```text
bronze.covid_owid_raw
bronze.gdp_world_bank_raw
bronze.health_centers_density_raw
bronze.hospital_beds_raw
bronze.hospital_density_raw
bronze.hospital_medicine_raw
```

It also creates:

```text
silver.covid_daily
```

The COVID-19 Silver table:

- Uses country and observation date as its intended grain.
- Casts dates and numeric measures to explicit data types.
- Retains raw, smoothed, cumulative, and per-million measures.
- Preserves missing values.
- Flags negative case and death reporting corrections.

## Prerequisites

You need:

- Git
- Databricks CLI version `0.258.0` or newer
- A Databricks workspace with Unity Catalog
- Permission to create catalogs, schemas, volumes, jobs, and pipelines
- Outbound access to Our World in Data and the World Bank

Databricks Free Edition is supported and uses serverless compute.

On macOS, install the Databricks CLI with:

```bash
brew install databricks/tap/databricks
databricks version
```

## Clone And Authenticate

Clone the repository:

```bash
git clone https://github.com/anthonycasarta/covid19-socioeconomic-analysis.git
cd covid19-socioeconomic-analysis
```

Create a local `.env` file:

```bash
DATABRICKS_HOST=https://<your-workspace-url>
```

The workspace URL is the base URL shown in your browser while using Databricks.

Load the environment variable:

```bash
set -a
source .env
set +a
```

Authenticate with Databricks:

```bash
databricks auth login \
  --host "$DATABRICKS_HOST" \
  --profile covid19-free
```

The profile name can be changed, but the same name must be used in later commands.

## First-Time Setup

Validate the bundle configuration:

```bash
databricks bundle validate \
  -t dev \
  -p covid19-free
```

Preview the resources that will be created:

```bash
databricks bundle plan \
  -t dev \
  -p covid19-free
```

Deploy only the setup job:

```bash
databricks bundle deploy \
  --select jobs.project_setup \
  -t dev \
  -p covid19-free
```

Run the setup job:

```bash
databricks bundle run project_setup \
  -t dev \
  -p covid19-free
```

The setup job creates:

- The `covid19_socioeconomic_analysis` catalog
- Bronze, Silver, and Gold schemas
- COVID-19, GDP, and healthcare volumes
- Required source directories

Deploy the complete bundle:

```bash
databricks bundle deploy \
  -t dev \
  -p covid19-free
```

Review the deployed jobs and pipeline:

```bash
databricks bundle summary \
  -t dev \
  -p covid19-free
```

Run the complete ETL workflow:

```bash
databricks bundle run socioeconomic_etl \
  -t dev \
  -p covid19-free
```

The ETL job lands all source data and then runs the Bronze-to-Silver pipeline automatically.

## Normal Runs

After the first-time setup, run only the ETL job:

```bash
databricks bundle run socioeconomic_etl \
  -t dev \
  -p covid19-free
```

The setup job does not need to run again unless the catalog, schemas, volumes, or source directories are removed.

## Development

After changing bundle resource files, validate and redeploy:

```bash
databricks bundle validate -t dev -p covid19-free
databricks bundle deploy -t dev -p covid19-free
```

For changes only to Python, SQL, or notebook source files, continuously synchronize them during development:

```bash
databricks bundle sync --watch \
  -t dev \
  -p covid19-free
```

Validate the pipeline without updating tables:

```bash
databricks bundle run socioeconomic_pipeline \
  --validate-only \
  -t dev \
  -p covid19-free
```

Pipeline validation requires the source files to have been landed first.

## Verification

List the Bronze and Silver tables:

```sql
SHOW TABLES IN covid19_socioeconomic_analysis.bronze;
SHOW TABLES IN covid19_socioeconomic_analysis.silver;
```

Check COVID-19 row counts:

```sql
SELECT COUNT(*) AS bronze_count
FROM covid19_socioeconomic_analysis.bronze.covid_owid_raw;
```

```sql
SELECT COUNT(*) AS silver_count
FROM covid19_socioeconomic_analysis.silver.covid_daily;
```

Check for duplicate country-date records:

```sql
SELECT
    country_code,
    observation_date,
    COUNT(*) AS record_count
FROM covid19_socioeconomic_analysis.silver.covid_daily
GROUP BY country_code, observation_date
HAVING COUNT(*) > 1;
```

## Known Limitations

- GDP and healthcare Silver transformations are not implemented.
- Country-date uniqueness is not enforced.
- Duplicate country-date records are not resolved.
- Country-code and valid-date filters remain disabled.
- The OWID endpoint provides a changing `latest` snapshot.
- Repeated complete snapshots require a replacement or versioning policy.
- Databricks Free Edition applies compute and pipeline quotas.
- Free Edition outbound internet access may be restricted.
- The project does not include automated tests.
- The datasets have not yet been joined or analyzed.

See `ROADMAP.md` for planned work.
````
