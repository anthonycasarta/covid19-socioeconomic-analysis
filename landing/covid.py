# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from landing.utils import download_as_csv_from_url_to_path

# COMMAND ----------

covid_csv_url = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
owid_covid_data_raw_dir = "/Volumes/covid19_socioeconomic_analysis/bronze/covid_raw/owid/data/"
owid_covid_file_name = "owid_covid_raw"

# COMMAND ----------

# COVID CSV
download_as_csv_from_url_to_path(covid_csv_url, owid_covid_data_raw_dir, owid_covid_file_name)


