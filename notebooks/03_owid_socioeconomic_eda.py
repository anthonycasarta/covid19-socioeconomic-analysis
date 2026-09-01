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

# COMMAND ----------

# MAGIC %md
# MAGIC # Analyze OWID Socioeconomic table
# MAGIC ---------
# MAGIC
# MAGIC ### Overview of take aways:

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Find Minimum Values of Numeric Columns
# MAGIC ----
# MAGIC
# MAGIC - Minimum values of 0 exist for numeric features. So, a null value does not mean 0, but must be imputed by some other method or dropped.

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     min(gdp_per_capita),
# MAGIC     min(extreme_poverty)
# MAGIC from
# MAGIC     owid_country_socioeconomic
# MAGIC ;