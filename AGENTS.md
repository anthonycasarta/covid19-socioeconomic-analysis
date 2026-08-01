# Agent Notes

- This repo is a Databricks notebook project, not a packaged Python app.
- The only active code is `notebooks/01_data_ingestion.py`; `notebooks/02_data_preprocessing.ipynb` is empty.
- The ingestion notebook reads COVID data from Our World in Data, GDP data from the World Bank, and healthcare CSVs from `dbfs:/Volumes/covid19_socioeconomic_analysis/default/tmp_healthcare_data/`.
- The committed CSVs in `data/` are not used by the notebook unless copied into that Databricks volume.
- There is no dependency manifest, test suite, CI workflow, or build config in the repo.
- Prefer verifying behavior from notebooks and source files over README prose when they differ.
- Preserve the current hard-coded Databricks paths unless the user asks to generalize them.
- Keep changes minimal and do not add scaffolding for missing tooling unless it is directly required.
