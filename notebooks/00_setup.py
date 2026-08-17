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

# MAGIC %md
# MAGIC ##Make data directories

# COMMAND ----------

# OWID Covid-19
owid_covid_data_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/covid_raw/owid/data/"
)
dbutils.fs.mkdirs(owid_covid_data_raw_dir)


# World Bank gdp_raw
world_bank_gdp_data_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/data/"
)
world_bank_gdp_metadata_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/metadata/"
)
dbutils.fs.mkdirs(world_bank_gdp_data_raw_dir)
dbutils.fs.mkdirs(world_bank_gdp_metadata_raw_dir)


# WHO Healthcare
who_healthcare_data_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/who/"
)
dbutils.fs.mkdirs(who_healthcare_data_raw_dir)

healthcare_data_dir_names = [
    "health_centers_density/",
    "hospital_beds/",
    "hospital_density/",
    "hospital_medicine/",
]
for dir_name in healthcare_data_dir_names:
    for sub_dir in ["data/", "metadata/"]:
        dbutils.fs.mkdirs(f"{who_healthcare_data_raw_dir}{dir_name}{sub_dir}")
