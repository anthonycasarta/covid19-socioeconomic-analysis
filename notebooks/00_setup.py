# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# Create Catalog
spark.sql(
    """
        CREATE CATALOG IF NOT EXISTS covid19_socioeconomic_analysis;
        """
)

# COMMAND ----------

# Create schemas
spark.sql(
    """
        CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.bronze;
        """
)

spark.sql(
    """
        CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.silver;
        """
)

spark.sql(
    """
        CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.gold;
        """
)
# COMMAND ----------

# Create volumes
spark.sql(
    """
        CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.bronze.covid_raw;
        """
)

spark.sql(
    """
        CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.bronze.gdp_raw;
        """
)

spark.sql(
    """
        CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.bronze.healthcare_raw;
        """
)
# COMMAND ----------

# Make data directories
owid_covid_data_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/covid_raw/owid/data/"
)
dbutils.fs.mkdirs(owid_covid_data_raw_dir)

world_bank_gdp_data_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/data/"
)
world_bank_gdp_metadata_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/metadata/"
)
dbutils.fs.mkdirs(world_bank_gdp_data_raw_dir)
dbutils.fs.mkdirs(world_bank_gdp_metadata_raw_dir)

who_healthcare_data_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/who/data/"
)
dbutils.fs.mkdirs(who_healthcare_data_raw_dir)
