# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from utils import get_response_content_from_url, write_response_content_as_file_to_path

# COMMAND ----------

covid_csv_url = (
    "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
)
owid_covid_data_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/covid_raw/owid/data/"
)
owid_covid_file_name = "owid_covid_raw"

# COMMAND ----------

# COVID CSV
response_content = get_response_content_from_url(covid_csv_url)
write_response_content_as_file_to_path(
    response_content, owid_covid_data_raw_dir, owid_covid_file_name, "csv"
)

# COMMAND ----------

covid_metadata_url = (
    "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.meta.json"
)
owid_covid_metadata_raw_dir = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/covid_raw/owid/metadata/"
)

# COVID CSV
response_content = get_response_content_from_url(covid_metadata_url)
write_response_content_as_file_to_path(
    response_content, owid_covid_metadata_raw_dir, "owid_covid_metadata", "json"
)