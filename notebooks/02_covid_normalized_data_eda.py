# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC ## Set Default Catalog and Schema

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG covid19_socioeconomic_analysis;
# MAGIC USE SCHEMA bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create a Temporary View consisting of only normalized metric data

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace temp view covid_normalized_metrics as
# MAGIC (
# MAGIC select
# MAGIC     country,
# MAGIC     date,
# MAGIC     new_cases_smoothed,
# MAGIC     total_cases_per_million,
# MAGIC     new_cases_per_million,
# MAGIC     new_cases_smoothed_per_million,
# MAGIC     new_deaths_smoothed,
# MAGIC     total_deaths_per_million,
# MAGIC     new_deaths_per_million,
# MAGIC     new_deaths_smoothed_per_million,
# MAGIC     total_tests_per_thousand,
# MAGIC     new_tests_per_thousand,
# MAGIC     new_tests_smoothed,
# MAGIC     new_tests_smoothed_per_thousand,
# MAGIC     total_vaccinations_per_hundred,
# MAGIC     people_vaccinated_per_hundred,
# MAGIC     people_fully_vaccinated_per_hundred,
# MAGIC     total_boosters_per_hundred,
# MAGIC     new_vaccinations_smoothed,
# MAGIC     new_vaccinations_smoothed_per_million,
# MAGIC     new_people_vaccinated_smoothed,
# MAGIC     new_people_vaccinated_smoothed_per_hundred,
# MAGIC     hosp_patients_per_million,
# MAGIC     weekly_hosp_admissions_per_million,
# MAGIC     icu_patients_per_million,
# MAGIC     weekly_icu_admissions_per_million,
# MAGIC     excess_mortality_cumulative_per_million
# MAGIC from covid_owid_raw
# MAGIC );
# MAGIC
# MAGIC select
# MAGIC     *
# MAGIC from 
# MAGIC     covid_normalized_metrics
# MAGIC limit
# MAGIC     10
# MAGIC ;

# COMMAND ----------

# MAGIC %md
# MAGIC # Analyze core normalized metric table
# MAGIC ---------
# MAGIC
# MAGIC ### Overview of take aways:

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Find Minimum Values of Numeric Columns
# MAGIC ----
# MAGIC
# MAGIC - The minimum values of the numeric columns are less than or equal to the value 0. That means that nulls cannot represent 0 values, confirming that null values are missing values and cannot be replaced with the value 0.

# COMMAND ----------

# MAGIC %sql
# MAGIC select 
# MAGIC     min(new_cases_smoothed) as min_new_cases_smoothed,
# MAGIC     min(total_cases_per_million) as min_total_cases_per_million,
# MAGIC     min(new_cases_per_million) as min_new_cases_per_million,
# MAGIC     min(new_cases_smoothed_per_million) as min_new_cases_smoothed_per_million,
# MAGIC     min(new_deaths_smoothed) as min_new_deaths_smoothed,
# MAGIC     min(total_deaths_per_million) as min_total_deaths_per_million,
# MAGIC     min(new_deaths_per_million) as min_new_deaths_per_million,
# MAGIC     min(new_deaths_smoothed_per_million) as min_new_deaths_smoothed_per_million,
# MAGIC     min(total_tests_per_thousand) as min_total_tests_per_thousand,
# MAGIC     min(new_tests_per_thousand) as min_new_tests_per_thousand,
# MAGIC     min(new_tests_smoothed) as min_new_tests_smoothed,
# MAGIC     min(new_tests_smoothed_per_thousand) as min_new_tests_smoothed_per_thousand,
# MAGIC     min(total_vaccinations_per_hundred) as min_total_vaccinations_per_hundred,
# MAGIC     min(people_vaccinated_per_hundred) as min_people_vaccinated_per_hundred,
# MAGIC     min(people_fully_vaccinated_per_hundred) as min_people_fully_vaccinated_per_hundred,
# MAGIC     min(total_boosters_per_hundred) as min_total_boosters_per_hundred,
# MAGIC     min(new_vaccinations_smoothed) as min_new_vaccinations_smoothed,
# MAGIC     min(new_vaccinations_smoothed_per_million) as min_new_vaccinations_smoothed_per_million,
# MAGIC     min(new_people_vaccinated_smoothed) as min_new_people_vaccinated_smoothed,
# MAGIC     min(new_people_vaccinated_smoothed_per_hundred) as min_new_people_vaccinated_smoothed_per_hundred,
# MAGIC     min(hosp_patients_per_million) as min_hosp_patients_per_million,
# MAGIC     min(weekly_hosp_admissions_per_million) as min_weekly_hosp_admissions_per_million,
# MAGIC     min(icu_patients_per_million) as min_icu_patients_per_million,
# MAGIC     min(weekly_icu_admissions_per_million) as min_weekly_icu_admissions_per_million,
# MAGIC     min(excess_mortality_cumulative_per_million) as min_excess_mortality_cumulative_per_million
# MAGIC from covid_normalized_metrics
# MAGIC ;