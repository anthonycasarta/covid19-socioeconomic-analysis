# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from utils import copy_csv_files_from_repo_to_volume

# COMMAND ----------

dbutils.widgets.text("source_dir", "")
source_dir = dbutils.widgets.get("source_dir")

# COMMAND ----------

who_healthcare_data_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/who/"
)

# COMMAND ----------

copy_csv_files_from_repo_to_volume(source_dir, who_healthcare_data_raw_dir)
