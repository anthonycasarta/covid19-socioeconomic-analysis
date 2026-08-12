# Roadmap

This file records the next likely project directions after the current ingestion and COVID Silver prototype.

## Completed

- Bronze ingestion now writes streaming tables for the source datasets.
- COVID-19 profiling and null-rate analysis are implemented.
- `silver.covid_daily` exists as a cleaned COVID-19 streaming table.

## Decision Summary

- Structured DB pulls: implement now as Delta table reads/writes inside Databricks.
- Telemetry: consider later if a good aggregated source supports the analysis.
- Recursive or hierarchical API traversal: skip for now.

## Structured DB Pulls

This is the best near-term fit for the remaining COVID work.

Use ingestion to write Bronze streaming tables, then have preprocessing read those tables with `spark.table(...)` instead of re-running notebook `%run` chains or re-fetching raw files.

Example shape:

```text
01_data_ingestion.py
  -> Bronze streaming tables
02_data_preprocessing_covid.py
  -> reads Bronze tables
  -> writes Silver tables
```

Why this fits:

- Reproducible snapshots
- Clear schema boundaries
- Easier preprocessing and debugging
- Better separation between raw ingestion and cleaning

If a real external database becomes available later, use JDBC only if it is authoritative and already maintained.

## Telemetry

Telemetry is optional and only makes sense if it answers a real analysis question.

Possible useful features:

- Country-level mobility changes by category
- Lockdown intensity or restriction response
- Recovery speed after restrictions

Constraints:

- Use only aggregated country- or region-level telemetry.
- Avoid individual-level or device-level data.
- Align telemetry to the same country codes and analysis period as the rest of the project.

Add telemetry only after the baseline country-level analysis is working and a reliable public aggregated source has been identified.

## Recursive or Hierarchical API Traversal

Do not force this into the project.

The current data sources are better handled through bulk or paginated endpoints than recursive discovery. Recursive traversal would add complexity without clear benefit unless a future source truly requires parent-child lookup.

Reconsider only if a source exposes useful nested resources that cannot be retrieved directly in bulk.

## Suggested Pipeline Shape

```text
APIs, CSVs, and other sources
            |
            v
Bronze raw snapshots in Delta
            |
            v
Silver cleaned and aligned tables
            |
            v
Gold country-level analysis table
```

## Recommended Order

1. Enable country-code and valid-date filters for COVID Silver.
2. Validate country-date uniqueness and define duplicate handling.
3. Add required-column and plausible-range checks for COVID Silver.
4. Verify refresh behavior when the OWID snapshot changes.
5. Standardize country codes and align observations.
6. Build the country-level analytical table.
7. Add telemetry only if it materially improves the analysis.
