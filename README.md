# COVID-19 Socioeconomic Analysis

A Databricks-oriented data project for studying relationships between COVID-19 mortality, economic conditions, and healthcare capacity across countries.

> **Project status:** Early development. Data ingestion is partially implemented, but preprocessing, dataset integration, statistical analysis, modeling, and visualization are not yet complete.

## Project Objective

The intended objective is to investigate whether differences in COVID-19 mortality across countries are associated with factors such as:

- GDP per capita
- Hospital-bed availability
- Hospital density
- Health-center density
- Availability and affordability of essential medicines

The project combines public COVID-19 and economic data with country-level healthcare indicators. Any eventual results should be interpreted as observational relationships rather than evidence of causation.

## Current Functionality

The current ingestion notebook:

- Downloads COVID-19 data from Our World in Data.
- Downloads GDP-per-capita data from the World Bank.
- Loads four healthcare indicator CSV files from a Databricks volume.
- Reads the remote datasets into pandas DataFrames.
- Converts the COVID-19 and GDP datasets into Spark DataFrames.
- Reads the healthcare datasets directly into Spark DataFrames.

The current implementation does **not** yet:

- Clean or validate the source data.
- Normalize country identifiers.
- Align observations by year.
- Calculate COVID-19 mortality metrics.
- Join the datasets.
- Handle missing or sparse observations.
- Perform statistical analysis or machine learning.
- Generate visualizations or reports.
- Persist processed datasets or model outputs.

## Repository Structure

```text
covid19-socioeconomic-analysis/
├── data/
│   ├── README.md
│   ├── health_centers_density.csv
│   ├── hospital_beds.csv
│   ├── hospital_density.csv
│   └── hospital_medicine.csv
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   └── 02_data_preprocessing.ipynb
├── scripts/
│   └── __init__.py
└── README.md
```

### Notebooks

#### `01_data_ingestion.ipynb`

Implements the current data-ingestion workflow.

It creates Spark DataFrames for:

- COVID-19 data
- GDP-per-capita data
- Hospital-bed availability
- Hospital density
- Health-center density
- Essential-medicine availability

#### `02_data_preprocessing.ipynb`

Reserved for preprocessing and dataset integration.

This notebook is currently empty.

## Data Sources

### COVID-19 Data

**Provider:** Our World in Data

**Current endpoint:**

```text
https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv
```

The endpoint uses the `latest` dataset, so its contents may change between executions.

The intended analysis will need to select and derive relevant variables such as:

- Total COVID-19 deaths
- Deaths per population
- Confirmed cases
- Population
- Observation date
- Country identifiers

No mortality metric is currently calculated by the project.

### GDP Per Capita

**Provider:** World Bank

**Indicator:** `NY.GDP.PCAP.CD`

**Description:** GDP per capita in current US dollars

**Current endpoint:**

```text
https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv
```

The World Bank file is downloaded as a ZIP archive and loaded into pandas.

The source data is organized with separate columns for individual years. It will need to be reshaped before it can be joined to the other datasets.

### Healthcare Indicators

The repository contains four healthcare indicator exports under `data/`.

Their structure and indicator naming suggest WHO-style indicator exports, but their exact provenance is not currently documented in the repository.

#### Hospital Beds

**File:** `data/hospital_beds.csv`

**Indicator:** Hospital beds per 10,000 population

The data contains observations covering approximately 2000 through 2021. The latest available year differs by country.

#### Hospital Density

**File:** `data/hospital_density.csv`

**Indicator:** Hospitals per 100,000 population

The available observations are predominantly from 2013, with limited 2014 coverage.

#### Health-Center Density

**File:** `data/health_centers_density.csv`

**Indicator:** Health centers per 100,000 population

The available observations primarily cover 2010 and 2013, with limited 2014 coverage.

#### Essential Medicines

**File:** `data/hospital_medicine.csv`

**Indicator:** Proportion of health facilities with a core set of relevant essential medicines available and affordable

This dataset is sparse and contains irregular observations from approximately 2004 through 2019. Some observations represent capital-city facilities rather than complete national coverage.

## Current Data Flow

```text
Our World in Data CSV
        |
        v
pandas COVID-19 DataFrame
        |
        v
Spark COVID-19 DataFrame

World Bank ZIP archive
        |
        v
pandas GDP DataFrame
        |
        v
Spark GDP DataFrame

Databricks healthcare CSVs
        |
        v
Four Spark healthcare DataFrames
```

The current pipeline ends after ingestion. The DataFrames are not yet joined or written to persistent storage.

## Databricks Environment

The project is designed to run in Databricks and assumes:

- An active Databricks cluster
- An existing Spark session
- Python with `pandas` and `requests`
- Outbound access to the OWID and World Bank endpoints
- Access to Unity Catalog volumes
- Permission to read the healthcare CSV files

The project does not currently include:

- A dependency manifest
- A Databricks Asset Bundle
- Cluster configuration
- Job or workflow definitions
- A local Spark configuration
- Automated environment setup

## Healthcare Data Location

The ingestion notebook expects the healthcare files at:

```text
dbfs:/Volumes/covid19_socioeconomic_analysis/default/tmp_healthcare_data/
```

The following files must exist in that location:

```text
health_centers_density.csv
hospital_beds.csv
hospital_density.csv
hospital_medicine.csv
```

Although copies of these files are committed under `data/`, the notebook does not automatically copy them to the Databricks volume.

## Running the Project

### Prerequisites

1. Import or synchronize the repository with a Databricks workspace.
2. Create or select a Databricks cluster.
3. Confirm that the runtime provides Spark, pandas, and requests.
4. Confirm that the cluster can access the OWID and World Bank endpoints.
5. Create or obtain access to the expected Databricks volume.
6. Upload the four healthcare CSV files to that volume.

### Notebook Execution

Run the notebooks in this order:

1. `notebooks/01_data_ingestion.ipynb`
2. `notebooks/02_data_preprocessing.ipynb`

The preprocessing notebook is currently empty, so only ingestion work is performed at this stage.

The project is not currently configured to run as a standalone local Python application.

## Planned Preprocessing

The preprocessing stage will need to address the following tasks.

### Country Standardization

Country names and codes differ across the source systems. Integration should use stable country identifiers wherever possible.

Potential tasks include:

- Selecting ISO country codes as the primary join key.
- Removing regional and aggregate World Bank records.
- Resolving countries with missing or inconsistent codes.
- Documenting any manual country mappings.

### Temporal Alignment

The datasets have substantially different coverage:

- COVID-19 data contains date-level observations.
- GDP data contains annual observations.
- Hospital-bed data contains multiple historical years.
- Hospital and health-center density data is largely from 2010–2014.
- Essential-medicine data is sparse and predates the pandemic.

A clear temporal policy is required, such as:

- Latest available pre-pandemic observation
- Nearest observation to 2019
- Nearest observation before the analyzed COVID-19 period
- Country-specific latest available observation with an age-of-data field

### Healthcare Indicator Selection

The healthcare exports may contain multiple records per country because of:

- Different reporting years
- Public- and private-sector coverage
- Country-specific latest-year flags
- Optional dimensions
- Differences in geographic coverage

The project will need explicit rules for selecting one representative value per country and indicator.

### COVID-19 Outcome Definition

A mortality outcome must be defined before analysis. Possible measures include:

- Cumulative deaths per million people
- Deaths per 100,000 people
- Case-fatality ratio
- Annual COVID-19 deaths per capita
- Maximum reported mortality during a specified period

The selected metric and observation period should be documented clearly.

### Missing Data

The healthcare datasets have uneven country coverage. The preprocessing pipeline should:

- Quantify missingness by feature.
- Avoid treating missing values as zero.
- Report how many countries remain after each join.
- Document any imputation strategy.
- Consider excluding indicators with insufficient coverage.

## Planned Analysis

Once preprocessing is complete, the project may include:

- Descriptive statistics
- Country and regional comparisons
- Correlation analysis
- Scatter plots and trend visualizations
- Regression analysis
- Sensitivity analysis for different temporal-alignment policies
- Assessment of missing-data and coverage bias
- Model evaluation and feature-importance analysis, if machine learning is used

Models should not be introduced until the data integration and target definitions are stable.

## Data-Quality Considerations

Several known issues require attention:

- The OWID endpoint points to a changing `latest` dataset.
- The World Bank ZIP member is currently selected by archive position.
- Spark schemas for healthcare files are inferred rather than declared.
- Some healthcare source strings contain character-encoding artifacts.
- Indicator units differ across datasets.
- `IsLatestYear` is country-specific and does not imply a common reporting year.
- Some healthcare records represent only public facilities, private facilities, or capital-city coverage.
- Healthcare observations often predate the COVID-19 pandemic by several years.
- The essential-medicine dataset has particularly limited country coverage.

## Reproducibility

The current ingestion process is not fully reproducible because:

- Remote datasets are not versioned or cached.
- The OWID URL changes over time.
- No source checksums are recorded.
- Dependency versions are not pinned.
- Spark schemas are inferred.
- No processed data snapshots are persisted.
- No automated tests validate source schemas or row counts.

Future development should consider:

- Pinning dependency versions.
- Recording data retrieval dates.
- Persisting raw source snapshots.
- Defining explicit Spark schemas.
- Validating required columns and expected value ranges.
- Writing processed datasets to versioned Delta tables.
- Adding data-quality and pipeline tests.

## Current Development Priorities

1. Implement `02_data_preprocessing.ipynb`.
2. Standardize country identifiers.
3. Define the COVID-19 mortality outcome and analysis period.
4. Reshape and filter the World Bank GDP data.
5. Select representative healthcare observations.
6. Join all datasets into a country-level analytical table.
7. Add data-quality checks and coverage reporting.
8. Persist the processed dataset.
9. Add exploratory analysis and visualizations.
10. Evaluate whether statistical or machine-learning models are justified.

## Limitations

The repository currently provides an ingestion prototype rather than a completed socioeconomic analysis.

No conclusions about relationships between GDP, healthcare capacity, and COVID-19 mortality should be drawn from the current implementation.
