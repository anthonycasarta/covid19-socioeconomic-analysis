# Databricks notebook source

import io
import zipfile

import pandas as pd
import requests

# MAGIC %md
# MAGIC Create catalog for project and schema and volume for healthcare data

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create covid19_socioeconomic_analysis Unity Catalog
# MAGIC CREATE CATALOG covid19_socioeconomic_analysis;
# MAGIC 
# MAGIC -- Create healthcare schema
# MAGIC CREATE SCHEMA covid19_socioeconomic_analysis.healthcare
# MAGIC
# MAGIC -- Create raw volume for healthcare schema
# MAGIC CREATE VOLUME covid19_socioeconomic_analysis.healthcare.raw

# COMMAND ----------

healthcare_data_path = "dbfs:/Volumes/covid19_socioeconomic_analysis/default/tmp_healthcare_data/"

# COMMAND ----------

health_centers_density_df = spark.read.csv(healthcare_data_path + "health_centers_density.csv", header=True, inferSchema=True)
hospital_beds_density_df = spark.read.csv(healthcare_data_path + "hospital_beds.csv", header=True, inferSchema=True)
hospital_density_df = spark.read.csv(healthcare_data_path + "hospital_density.csv", header=True, inferSchema=True)
hospital_medicine_df = spark.read.csv(healthcare_data_path + "hospital_medicine.csv", header=True, inferSchema=True)

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
