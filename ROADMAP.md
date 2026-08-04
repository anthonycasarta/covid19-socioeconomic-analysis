# Roadmap

This file records the next likely project directions after the current ingestion prototype.

## Decision Summary

- Structured DB pulls: implement now as Delta table reads/writes inside Databricks.
- Telemetry: consider later if a good aggregated source supports the analysis.
- Recursive or hierarchical API traversal: skip for now.

## Structured DB Pulls

This is the best near-term fit for the project.

Use ingestion to write Bronze Delta tables, then have preprocessing read those tables with `spark.table(...)` instead of re-running notebook `%run` chains or re-fetching raw files.

Example shape:

```text
01_data_ingestion.py
  -> Bronze Delta tables
02_data_preprocessing.py
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

1. Complete the baseline preprocessing pipeline.
2. Persist ingestion outputs to Bronze Delta tables.
3. Read Bronze tables from preprocessing.
4. Standardize country codes and align observations.
5. Build the country-level analytical table.
6. Add telemetry only if it materially improves the analysis.
