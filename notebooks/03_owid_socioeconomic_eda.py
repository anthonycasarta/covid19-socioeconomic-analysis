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

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. List all distinct countries in the dataset
# MAGIC ---
# MAGIC
# MAGIC - Some countries are reused or grouped with other countries. Where possible, each row will only consist of one country. Exclude countries: Asia excl. China; World; World excl. China; World excl. China, South Korea; World excl. China, South Korea, Japan and Singapore; Winter Olympics 2022; Summer Olympics 2020; Low-income countries; Lower-middle-income countries; High-income countries; European Union (27).
# MAGIC
# MAGIC - The countries grouped, such as: Low-income countries, Lower-middle-income countries, and so on can perhaps be used in the future once we categorize the countries as falling into one of these groups. That is to say, we can analyze how our classifications compare to the ones that the dataset includes.

# COMMAND ----------

# MAGIC %sql
# MAGIC select distinct
# MAGIC     country
# MAGIC from
# MAGIC     owid_country_socioeconomic
# MAGIC order by
# MAGIC     country
# MAGIC ;