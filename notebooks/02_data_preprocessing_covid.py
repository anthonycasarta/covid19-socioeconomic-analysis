# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %run ./01_data_ingestion

# COMMAND ----------

# MAGIC %md
# MAGIC ##Review Covid data

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM covid19_socioeconomic_analysis.bronze.covid_owid_raw
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE EXTENDED covid19_socioeconomic_analysis.bronze.covid_owid_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Get record count of Covid data
# MAGIC SELECT COUNT(*) AS record_count
# MAGIC FROM covid19_socioeconomic_analysis.bronze.covid_owid_raw;

# COMMAND ----------

# DBTITLE 1,Calculate null rates for all columns

# Calculate null rates for all columns
from pyspark.sql.functions import col, count, when, round as spark_round

# Read the table
df = spark.table("covid19_socioeconomic_analysis.bronze.covid_owid_raw")

# Calculate null counts for all columns
total_count = df.count()
null_stats = df.select([
    count(when(col(c).isNull(), c)).alias(c) 
    for c in df.columns
]).collect()[0]

# Convert to a DataFrame for display
from pyspark.sql import Row
results = [
    Row(
        column_name=c,
        null_count=null_stats[c],
        total_count=total_count,
        null_rate=round(null_stats[c] / total_count, 4)
    )
    for c in df.columns
]

null_rate_df = spark.createDataFrame(results).orderBy("null_rate", ascending=False)
display(null_rate_df)

# COMMAND ----------

from pyspark.sql.functions import col

acceptable_null_rate_columns = [
    row.column_name
    for row in null_rate_df.filter(
        (col("null_rate") <= 0.4) & (~col("column_name").rlike("_rescued_data"))
    ).collect()
]

display(acceptable_null_rate_columns)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create silver schema
# MAGIC CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.silver;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REFRESH STREAMING TABLE
# MAGIC     covid19_socioeconomic_analysis.silver.covid_daily
# MAGIC COMMENT 'Cleaned daily country-level COVID-19 time-series data'
# MAGIC AS
# MAGIC SELECT
# MAGIC     UPPER(TRIM(code)) AS country_code,
# MAGIC     TRIM(country) AS country_name,
# MAGIC     TRIM(continent) AS continent,
# MAGIC     TRY_CAST(`date` AS DATE) AS observation_date,
# MAGIC
# MAGIC     -- Country attributes
# MAGIC     TRY_CAST(population AS BIGINT) AS population,
# MAGIC     TRY_CAST(population_density AS DOUBLE) AS population_density,
# MAGIC     TRY_CAST(median_age AS DOUBLE) AS median_age,
# MAGIC     TRY_CAST(life_expectancy AS DOUBLE) AS life_expectancy,
# MAGIC     TRY_CAST(gdp_per_capita AS DOUBLE) AS gdp_per_capita,
# MAGIC     TRY_CAST(extreme_poverty AS DOUBLE) AS extreme_poverty,
# MAGIC     TRY_CAST(diabetes_prevalence AS DOUBLE) AS diabetes_prevalence,
# MAGIC     TRY_CAST(hospital_beds_per_thousand AS DOUBLE)
# MAGIC         AS hospital_beds_per_thousand,
# MAGIC
# MAGIC     -- Daily cases
# MAGIC     TRY_CAST(new_cases AS DOUBLE) AS new_cases,
# MAGIC     TRY_CAST(new_cases_per_million AS DOUBLE)
# MAGIC         AS new_cases_per_million,
# MAGIC     TRY_CAST(new_cases_smoothed AS DOUBLE)
# MAGIC         AS new_cases_smoothed,
# MAGIC     TRY_CAST(new_cases_smoothed_per_million AS DOUBLE)
# MAGIC         AS new_cases_smoothed_per_million,
# MAGIC
# MAGIC     -- Cumulative cases
# MAGIC     TRY_CAST(total_cases AS DOUBLE) AS total_cases,
# MAGIC     TRY_CAST(total_cases_per_million AS DOUBLE)
# MAGIC         AS total_cases_per_million,
# MAGIC
# MAGIC     -- Daily deaths
# MAGIC     TRY_CAST(new_deaths AS DOUBLE) AS new_deaths,
# MAGIC     TRY_CAST(new_deaths_per_million AS DOUBLE)
# MAGIC         AS new_deaths_per_million,
# MAGIC     TRY_CAST(new_deaths_smoothed AS DOUBLE)
# MAGIC         AS new_deaths_smoothed,
# MAGIC     TRY_CAST(new_deaths_smoothed_per_million AS DOUBLE)
# MAGIC         AS new_deaths_smoothed_per_million,
# MAGIC
# MAGIC     -- Cumulative deaths
# MAGIC     TRY_CAST(total_deaths AS DOUBLE) AS total_deaths,
# MAGIC     TRY_CAST(total_deaths_per_million AS DOUBLE)
# MAGIC         AS total_deaths_per_million,
# MAGIC     COALESCE(new_cases < 0, FALSE)
# MAGIC         AS has_negative_case_correction,
# MAGIC     COALESCE(new_deaths < 0, FALSE)
# MAGIC         AS has_negative_death_correction
# MAGIC
# MAGIC FROM STREAM
# MAGIC     covid19_socioeconomic_analysis.bronze.covid_owid_raw;
# MAGIC -- WHERE country_code RLIKE '^[A-Z]{3}$'
# MAGIC --     AND observation_date IS NOT NULL;
# MAGIC     
# MAGIC     

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM covid19_socioeconomic_analysis.silver.covid_daily
# MAGIC LIMIT 50;