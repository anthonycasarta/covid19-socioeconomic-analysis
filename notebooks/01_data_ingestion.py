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
# MAGIC ##Create Structure for Project Data

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create covid19_socioeconomic_analysis Unity Catalog
# MAGIC CREATE CATALOG IF NOT EXISTS covid19_socioeconomic_analysis;
# MAGIC
# MAGIC -- Create bronze schema
# MAGIC CREATE SCHEMA IF NOT EXISTS covid19_socioeconomic_analysis.bronze;
# MAGIC
# MAGIC -- Create raw volumes for bronze schema
# MAGIC CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.bronze.healthcare_raw;
# MAGIC CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.bronze.covid_raw;
# MAGIC CREATE VOLUME IF NOT EXISTS covid19_socioeconomic_analysis.bronze.gdp_raw;

# COMMAND ----------

# MAGIC %md
# MAGIC ##Move healthcare data from project files to the raw volume

# COMMAND ----------

healthcare_data_raw_dir = "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/"

# COMMAND ----------

user = spark.sql("SELECT current_user()").first()[0]
source_dir = f"/Workspace/Users/{user}/covid19-socioeconomic-analysis/data/"
base_dir = f"{healthcare_data_raw_dir}source_a/data/"

target_dir = base_dir
dbutils.fs.mkdirs(base_dir)

for f in dbutils.fs.ls(source_dir):
    if f.path.endswith(".csv"):
        dbutils.fs.cp(f.path, target_dir + f.name)

# COMMAND ----------

# MAGIC %md
# MAGIC ##Download Covid-19 and GDP data into raw volumes

# COMMAND ----------

covid_csv_url = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
gdp_csv_url = "https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv"

# COMMAND ----------

owid_covid_data_raw_dir = "/Volumes/covid19_socioeconomic_analysis/bronze/covid_raw/owid/data/"
world_bank_gdp_data_raw_dir = "/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/data/"
world_bank_gdp_metadata_raw_dir = "/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/metadata/"

# COMMAND ----------

# COVID CSV
dbutils.fs.mkdirs(owid_covid_data_raw_dir)

r = requests.get(covid_csv_url, timeout=60)
r.raise_for_status()
with open(owid_covid_data_raw_dir + "owid_covid_19_compact.csv", "wb") as f:
    f.write(r.content)

# GDP ZIP
dbutils.fs.mkdirs(world_bank_gdp_data_raw_dir)
dbutils.fs.mkdirs(world_bank_gdp_metadata_raw_dir)

r = requests.get(gdp_csv_url, timeout=60)
r.raise_for_status()
with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    for name in z.namelist():
        base = name.split("/")[-1]

        if base.startswith("Metadata_") or not base.endswith(".csv"):
            with z.open(name) as src, open(world_bank_gdp_metadata_raw_dir + base, "wb") as dst:
                dst.write(src.read())
            continue

        with z.open(name) as src, open(world_bank_gdp_data_raw_dir + "world_bank_gdp_per_capita.csv", "wb") as dst:
            dst.write(src.read())

# COMMAND ----------

# MAGIC %md
# MAGIC ##Ingest into Delta Tables

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Health Centers Density
# MAGIC CREATE OR REFRESH STREAMING TABLE IF NOT EXISTS 
# MAGIC covid19_socioeconomic_analysis.bronze.health_centers_density_raw
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files()

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Hospital Beds
# MAGIC CREATE OR REFRESH STREAMING TABLE IF NOT EXISTS 
# MAGIC covid19_socioeconomic_analysis.bronze.hospital_beds_raw
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files()

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Hospital Density
# MAGIC CREATE OR REFRESH STREAMING TABLE IF NOT EXISTS 
# MAGIC covid19_socioeconomic_analysis.bronze.hospital_density_raw
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files()

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Hospital Medicine
# MAGIC CREATE OR REFRESH STREAMING TABLE IF NOT EXISTS 
# MAGIC covid19_socioeconomic_analysis.bronze.hospital_medicine_raw
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files()

# COMMAND ----------

# MAGIC %sql
# MAGIC -- COVID
# MAGIC CREATE OR REFRESH STREAMING TABLE IF NOT EXISTS
# MAGIC covid19_socioeconomic_analysis.bronze.covid_owid_raw
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files()

# COMMAND ----------

# MAGIC %sql
# MAGIC -- GDP
# MAGIC CREATE OR REFRESH STREAMING TABLE IF NOT EXISTS
# MAGIC covid19_socioeconomic_analysis.bronze.gdp_world_bank_raw
# MAGIC AS SELECT *
# MAGIC FROM STREAM read_files()

