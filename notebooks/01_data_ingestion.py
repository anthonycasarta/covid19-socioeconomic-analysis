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
# MAGIC ##Create catalog for project and schema and volume for healthcare data

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create covid19_socioeconomic_analysis Unity Catalog
# MAGIC CREATE CATALOG IF NOT EXISTS covid19_socioeconomic_analysis;
# MAGIC
# MAGIC -- Create healthcare schema
# MAGIC CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.healthcare;
# MAGIC
# MAGIC -- Create raw volume for healthcare schema
# MAGIC CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.healthcare.raw;

# COMMAND ----------

# MAGIC %md
# MAGIC ##Move healthcare data from project files to the raw volume

# COMMAND ----------

healthcare_data_raw_dir = "/Volumes/covid19_socioeconomic_analysis/healthcare/raw/"

# COMMAND ----------

user = spark.sql("SELECT current_user()").first()[0]
source_dir = f"/Workspace/Users/{user}/covid19-socioeconomic-analysis/data/"
target_dir = healthcare_data_raw_dir

for f in dbutils.fs.ls(source_dir):
    if f.path.endswith(".csv"):
        dbutils.fs.cp(f.path, target_dir + f.name)

# COMMAND ----------

# MAGIC %md
# MAGIC ##Create schemas and volumes for Covid-19 and GDP data

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create covid_19 schema
# MAGIC CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.covid_19;
# MAGIC
# MAGIC -- Create raw volume for covid_19 schema
# MAGIC CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.covid_19.raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create gdp schema
# MAGIC CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.gdp;
# MAGIC
# MAGIC -- Create raw volume for gdp schema
# MAGIC CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.gdp.raw;

# COMMAND ----------

# MAGIC %md
# MAGIC ##Download Covid-19 and GDP data into raw volumes

# COMMAND ----------

covid_csv_url = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
gdp_csv_url = "https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv"

# COMMAND ----------

covid_data_raw_dir = "/Volumes/covid19_socioeconomic_analysis/covid_19/raw/"
gdp_data_raw_dir = "/Volumes/covid19_socioeconomic_analysis/gdp/raw/"

# COMMAND ----------

# COVID CSV
r = requests.get(covid_csv_url, timeout=60)
r.raise_for_status()
with open(covid_data_raw_dir + "owid_covid_19_compact.csv", "wb") as f:
    f.write(r.content)

# GDP ZIP
r = requests.get(gdp_csv_url, timeout=60)
r.raise_for_status()
with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    csv_name = next(
        name for name in z.namelist()
        if name.endswith(".csv") and not name.split("/")[-1].startswith("Metadata_")
    )
    with z.open(csv_name) as src, open(gdp_data_raw_dir + "world_bank_gdp_per_capita.csv", "wb") as dst:
        dst.write(src.read())

# COMMAND ----------

covid_df = spark.createDataFrame(covid_pdf)
gdp_df = spark.createDataFrame(gdp_pdf)
