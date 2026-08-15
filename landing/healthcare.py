# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
dbutils.widgets.text("source_dir", "")
source_dir = dbutils.widgets.get("source_dir")

# COMMAND ----------

who_healthcare_data_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/who/"
)
base_dir = f"{who_healthcare_data_raw_dir}source_a/"

target_dir = base_dir

# COMMAND ----------

for f in dbutils.fs.ls(source_dir):
    if f.path.endswith(".csv"):
        dbutils.fs.cp(
            f.path, f"{target_dir}/{f.name.removesuffix('.csv')}/data/" + f.name
        )
