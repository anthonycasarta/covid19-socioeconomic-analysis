# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC ## Set Default Catalog and Schema

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog covid19_socioeconomic_analysis;
# MAGIC use schema bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create a Temporary View consisting of only scocioeconomic related data by country

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace temp view owid_country_socioeconomic as
# MAGIC (
# MAGIC     select
# MAGIC         country,
# MAGIC         date,
# MAGIC         gdp_per_capita,
# MAGIC         extreme_poverty
# MAGIC     from covid_owid_raw
# MAGIC );
# MAGIC
# MAGIC select
# MAGIC     *
# MAGIC from 
# MAGIC     owid_country_socioeconomic
# MAGIC limit
# MAGIC     10
# MAGIC ;