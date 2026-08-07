# Databricks notebook source
# MAGIC %run ./01_data_ingestion

# COMMAND ---------- 

# MAGIC %md
# MAGIC #Review Covid data

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS record_count
# MAGIC FROM covid19_socioeconomic_analysis.bronze.covid_owid_raw;
