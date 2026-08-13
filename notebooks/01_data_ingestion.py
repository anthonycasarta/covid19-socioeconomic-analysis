# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# COMMAND ----------

# MAGIC %md
# MAGIC ##Ingest into Delta Tables

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Health Centers Density
# MAGIC CREATE OR REFRESH STREAMING TABLE
# MAGIC covid19_socioeconomic_analysis.bronze.health_centers_density_raw
# MAGIC TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files(
# MAGIC     "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/source_a/health_centers_density/data/",
# MAGIC     format => "csv",
# MAGIC     header => true
# MAGIC     )

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Hospital Beds
# MAGIC CREATE OR REFRESH STREAMING TABLE
# MAGIC covid19_socioeconomic_analysis.bronze.hospital_beds_raw
# MAGIC TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files(
# MAGIC     "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/source_a/hospital_beds/data/",
# MAGIC     format => 'csv',
# MAGIC     header => true
# MAGIC     )

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Hospital Density
# MAGIC CREATE OR REFRESH STREAMING TABLE
# MAGIC covid19_socioeconomic_analysis.bronze.hospital_density_raw
# MAGIC TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files(
# MAGIC     "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/source_a/hospital_density/data/",
# MAGIC     format => 'csv',
# MAGIC     header => true
# MAGIC     )

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Hospital Medicine
# MAGIC CREATE OR REFRESH STREAMING TABLE
# MAGIC covid19_socioeconomic_analysis.bronze.hospital_medicine_raw
# MAGIC TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files(
# MAGIC     "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/source_a/hospital_medicine/data/",
# MAGIC     format => 'csv',
# MAGIC     header => true
# MAGIC     )

# COMMAND ----------

# MAGIC %sql
# MAGIC -- COVID
# MAGIC CREATE OR REFRESH STREAMING TABLE
# MAGIC covid19_socioeconomic_analysis.bronze.covid_owid_raw
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files(
# MAGIC     "/Volumes/covid19_socioeconomic_analysis/bronze/covid_raw/owid/data/",
# MAGIC     format => "csv",
# MAGIC     header => true,
# MAGIC     )

# COMMAND ----------

# MAGIC %sql
# MAGIC -- GDP
# MAGIC CREATE OR REFRESH STREAMING TABLE
# MAGIC covid19_socioeconomic_analysis.bronze.gdp_world_bank_raw
# MAGIC TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files("/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/data/")
# MAGIC

