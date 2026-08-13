# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
user = spark.sql("SELECT current_user()").first()[0]

# COMMAND ----------

who_healthcare_data_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/who/"
)
source_dir = f"/Workspace/Users/{user}/covid19-socioeconomic-analysis/data/"
base_dir = f"{who_healthcare_data_raw_dir}source_a/"

target_dir = base_dir

# COMMAND ----------

for f in dbutils.fs.ls(source_dir):
    if f.path.endswith(".csv"):
        dbutils.fs.cp(
            f.path, f"{target_dir}/{f.name.removesuffix('.csv')}/data/" + f.name
        )
