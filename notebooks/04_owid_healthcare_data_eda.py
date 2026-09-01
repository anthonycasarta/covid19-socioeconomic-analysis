# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
import plotly.express as px

# COMMAND ----------

# MAGIC %md
# MAGIC ## Set Default Catalog and Schema

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog covid19_socioeconomic_analysis;
# MAGIC use schema bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create a Temporary View consisting of only healthcare related data by country

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace temp view owid_country_healthcare as
# MAGIC (
# MAGIC     select
# MAGIC         country,
# MAGIC         date,
# MAGIC         population_density,
# MAGIC         median_age,
# MAGIC         life_expectancy,
# MAGIC         diabetes_prevalence,
# MAGIC         handwashing_facilities,
# MAGIC         hospital_beds_per_thousand,
# MAGIC         human_development_index
# MAGIC     from covid_owid_raw
# MAGIC );
# MAGIC
# MAGIC select
# MAGIC     *
# MAGIC from 
# MAGIC     owid_country_healthcare
# MAGIC limit
# MAGIC     10
# MAGIC ;