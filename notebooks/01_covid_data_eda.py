# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %sql
# MAGIC USE CATALOG covid19_socioeconomic_analysis;
# MAGIC USE SCHEMA bronze;

# COMMAND ----------

# DBTITLE 1,Binary null indicators for all columns
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   covid_owid_raw
# MAGIC LIMIT
# MAGIC     10
# MAGIC ;

# COMMAND ----------

# DBTITLE 1,Create bronze table: Core metrics
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE covid_core_metrics AS
# MAGIC SELECT
# MAGIC     country,
# MAGIC     date,
# MAGIC     code,
# MAGIC     continent,
# MAGIC     population,
# MAGIC     total_cases,
# MAGIC     new_cases,
# MAGIC     total_deaths,
# MAGIC     new_deaths,
# MAGIC     total_tests,
# MAGIC     new_tests,
# MAGIC     positive_rate,
# MAGIC     tests_per_case,
# MAGIC     total_vaccinations,
# MAGIC     people_vaccinated,
# MAGIC     people_fully_vaccinated,
# MAGIC     total_boosters,
# MAGIC     new_vaccinations,
# MAGIC     hosp_patients,
# MAGIC     weekly_hosp_admissions,
# MAGIC     icu_patients,
# MAGIC     weekly_icu_admissions,
# MAGIC     excess_mortality,
# MAGIC     excess_mortality_cumulative,
# MAGIC     excess_mortality_cumulative_absolute,
# MAGIC     stringency_index,
# MAGIC     reproduction_rate
# MAGIC FROM covid_owid_raw

# COMMAND ----------

# DBTITLE 1,Create bronze table: Normalized metrics
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE covid_normalized_metrics AS
# MAGIC SELECT
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
# MAGIC FROM covid_owid_raw

# COMMAND ----------

# DBTITLE 1,Create bronze table: Healthcare demographics
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE owid_country_healthcare AS
# MAGIC SELECT
# MAGIC     country,
# MAGIC     date,
# MAGIC     population_density,
# MAGIC     median_age,
# MAGIC     life_expectancy,
# MAGIC     diabetes_prevalence,
# MAGIC     handwashing_facilities,
# MAGIC     hospital_beds_per_thousand,
# MAGIC     human_development_index
# MAGIC FROM covid_owid_raw

# COMMAND ----------

# DBTITLE 1,Create bronze table: Socioeconomic indicators
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE owid_country_socioeconomic AS
# MAGIC SELECT
# MAGIC     country,
# MAGIC     date,
# MAGIC     gdp_per_capita,
# MAGIC     extreme_poverty
# MAGIC FROM covid_owid_raw

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     *
# MAGIC from
# MAGIC     hospital_beds_raw
# MAGIC
# MAGIC ;

# COMMAND ----------

# DBTITLE 1,Null analysis: Core metrics by date
# MAGIC %sql
# MAGIC -- Null rates over time by month (wide format for easy multi-line charting)
# MAGIC with covid_core_nulls as
# MAGIC (
# MAGIC     select
# MAGIC         date_trunc('MONTH', date) as month,
# MAGIC         case when country is null then 1 else 0 end as country_null,
# MAGIC         case when code is null then 1 else 0 end as code_null,
# MAGIC         case when continent is null then 1 else 0 end as continent_null,
# MAGIC         case when population is null then 1 else 0 end as population_null,
# MAGIC         case when total_cases is null then 1 else 0 end as total_cases_null,
# MAGIC         case when new_cases is null then 1 else 0 end as new_cases_null,
# MAGIC         case when total_deaths is null then 1 else 0 end as total_deaths_null,
# MAGIC         case when new_deaths is null then 1 else 0 end as new_deaths_null,
# MAGIC         case when total_tests is null then 1 else 0 end as total_tests_null,
# MAGIC         case when new_tests is null then 1 else 0 end as new_tests_null,
# MAGIC         case when positive_rate is null then 1 else 0 end as positive_rate_null,
# MAGIC         case when tests_per_case is null then 1 else 0 end as tests_per_case_null,
# MAGIC         case when total_vaccinations is null then 1 else 0 end as total_vaccinations_null,
# MAGIC         case when people_vaccinated is null then 1 else 0 end as people_vaccinated_null,
# MAGIC         case when people_fully_vaccinated is null then 1 else 0 end as people_fully_vaccinated_null,
# MAGIC         case when total_boosters is null then 1 else 0 end as total_boosters_null,
# MAGIC         case when new_vaccinations is null then 1 else 0 end as new_vaccinations_null,
# MAGIC         case when hosp_patients is null then 1 else 0 end as hosp_patients_null,
# MAGIC         case when weekly_hosp_admissions is null then 1 else 0 end as weekly_hosp_admissions_null,
# MAGIC         case when icu_patients is null then 1 else 0 end as icu_patients_null,
# MAGIC         case when weekly_icu_admissions is null then 1 else 0 end as weekly_icu_admissions_null,
# MAGIC         case when excess_mortality is null then 1 else 0 end as excess_mortality_null,
# MAGIC         case when excess_mortality_cumulative is null then 1 else 0 end as excess_mortality_cumulative_null,
# MAGIC         case when excess_mortality_cumulative_absolute is null then 1 else 0 end as excess_mortality_cumulative_absolute_null,
# MAGIC         case when stringency_index is null then 1 else 0 end as stringency_index_null,
# MAGIC         case when reproduction_rate is null then 1 else 0 end as reproduction_rate_null
# MAGIC     from covid_core_metrics
# MAGIC )
# MAGIC select
# MAGIC     month,
# MAGIC     avg(country_null) as country_null_rate,
# MAGIC     avg(code_null) as code_null_rate,
# MAGIC     avg(continent_null) as continent_null_rate,
# MAGIC     avg(population_null) as population_null_rate,
# MAGIC     avg(total_cases_null) as total_cases_null_rate,
# MAGIC     avg(new_cases_null) as new_cases_null_rate,
# MAGIC     avg(total_deaths_null) as total_deaths_null_rate,
# MAGIC     avg(new_deaths_null) as new_deaths_null_rate,
# MAGIC     avg(total_tests_null) as total_tests_null_rate,
# MAGIC     avg(new_tests_null) as new_tests_null_rate,
# MAGIC     avg(positive_rate_null) as positive_rate_null_rate,
# MAGIC     avg(tests_per_case_null) as tests_per_case_null_rate,
# MAGIC     avg(total_vaccinations_null) as total_vaccinations_null_rate,
# MAGIC     avg(people_vaccinated_null) as people_vaccinated_null_rate,
# MAGIC     avg(people_fully_vaccinated_null) as people_fully_vaccinated_null_rate,
# MAGIC     avg(total_boosters_null) as total_boosters_null_rate,
# MAGIC     avg(new_vaccinations_null) as new_vaccinations_null_rate,
# MAGIC     avg(hosp_patients_null) as hosp_patients_null_rate,
# MAGIC     avg(weekly_hosp_admissions_null) as weekly_hosp_admissions_null_rate,
# MAGIC     avg(icu_patients_null) as icu_patients_null_rate,
# MAGIC     avg(weekly_icu_admissions_null) as weekly_icu_admissions_null_rate,
# MAGIC     avg(excess_mortality_null) as excess_mortality_null_rate,
# MAGIC     avg(excess_mortality_cumulative_null) as excess_mortality_cumulative_null_rate,
# MAGIC     avg(excess_mortality_cumulative_absolute_null) as excess_mortality_cumulative_absolute_null_rate,
# MAGIC     avg(stringency_index_null) as stringency_index_null_rate,
# MAGIC     avg(reproduction_rate_null) as reproduction_rate_null_rate
# MAGIC from covid_core_nulls
# MAGIC group by month
# MAGIC order by month;