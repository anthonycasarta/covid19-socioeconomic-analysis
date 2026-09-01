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

# COMMAND ----------

# MAGIC %md
# MAGIC # Analyze core metric table
# MAGIC ---------
# MAGIC
# MAGIC ### Overview of take aways:

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Find Minimum Values of Numeric Columns
# MAGIC ----
# MAGIC
# MAGIC - There aren't any values that are less than or equal to 0. However, the assumption cannot be made that a null value is actually a value of 0. Considering all other values that come from the original dataset have null values as missing data, that will be the assumption for these null values. That is to say, the null values must be imputed or dropped as has been the case with the other data from the originating dataset.

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     min(population_density) as min_population_density,
# MAGIC     min(median_age) as min_median_age,
# MAGIC     min(life_expectancy) as min_life_expectancy,
# MAGIC     min(diabetes_prevalence) as min_diabetes_prevalence,
# MAGIC     min(handwashing_facilities) as min_handwashing_facilities,
# MAGIC     min(hospital_beds_per_thousand) as min_hospital_beds_per_thousand,
# MAGIC     min(human_development_index) as min_human_development_index
# MAGIC from
# MAGIC     owid_country_healthcare
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
# MAGIC     owid_country_healthcare
# MAGIC order by
# MAGIC     country
# MAGIC ;