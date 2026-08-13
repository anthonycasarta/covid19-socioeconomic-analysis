# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# Create Catalog
spark.sql(
        '''
        CREATE CATALOG IF NOT EXISTS covid19_socioeconomic_analysis;
        '''
        )

# COMMAND ----------

# Create schemas
spark.sql(
        '''
        CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.bronze;
        CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.silver;
        CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.gold;
        '''
        )

# COMMAND ----------

# Create volumes
spark.sql(
        '''
        CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.bronze.covid_raw;
        CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.bronze.gdp_raw;
        CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.bronze.healthcare_raw;
        '''
        )
