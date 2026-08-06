# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
import io
import zipfile

import pandas as pd
import requests

# COMMAND ----------

# MAGIC %md
# MAGIC Create catalog for project and schema and volume for healthcare data

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create covid19_socioeconomic_analysis Unity Catalog
# MAGIC CREATE CATALOG covid19_socioeconomic_analysis;
# MAGIC
# MAGIC -- Create healthcare schema
# MAGIC CREATE SCHEMA covid19_socioeconomic_analysis.healthcare;
# MAGIC
# MAGIC -- Create raw volume for healthcare schema
# MAGIC CREATE VOLUME covid19_socioeconomic_analysis.healthcare.raw;

# COMMAND ----------

# MAGIC %md
# MAGIC Move healthcare data from project files to the raw volume

# COMMAND ----------

healthcare_data_raw_dir = "/Volumes/covid19_socioeconomic_analysis/healthcare/raw"

# COMMAND ----------

user = spark.sql("SELECT current_user()").first()[0]
source__dir = "/Workspace/Users/{user}/covid19-socioeconomic-analysis/data"
target_dir = healthcare_data_raw_dir

for f in dbutils.fs.ls(source_dir):
    if f.path.endswith(".csv"):
        dbutils.fs.cp(f.path, target_dir + f.name)

# COMMAND ----------

covid_csv_url = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
gdp_csv_url = "https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv"

covid_pdf = pd.read_csv(covid_csv_url)
response = requests.get(gdp_csv_url)
response.raise_for_status()

with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    print(z.namelist())

    csv_filename = z.namelist()[1]

    gdp_pdf = pd.read_csv(z.open(csv_filename), skiprows=4)

# COMMAND ----------

covid_df = spark.createDataFrame(covid_pdf)
gdp_df = spark.createDataFrame(gdp_pdf)
