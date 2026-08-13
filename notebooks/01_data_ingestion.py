# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# COMMAND ----------

# MAGIC %md
# MAGIC ##Ingest into Delta Tables

# COMMAND ----------


# COMMAND ----------

# MAGIC %sql
# MAGIC -- GDP
# MAGIC CREATE OR REFRESH STREAMING TABLE
# MAGIC covid19_socioeconomic_analysis.bronze.gdp_world_bank_raw
# MAGIC TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files("/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/data/")
# MAGIC

