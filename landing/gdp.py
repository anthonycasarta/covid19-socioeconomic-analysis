# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from pathlib import Path

from utils import (
    get_response_content_from_url,
    unzip_response_content,
    write_response_content_as_csv_to_path,
)

# COMMAND ----------

GDP_CSV_URL = (
    "https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv"
)

GDP_DATA_RAW_DIR = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/data/"
)

GDP_METADATA_RAW_DIR = (
    "/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/metadata/"
)

# COMMAND ----------

response_content = get_response_content_from_url(GDP_CSV_URL)
extracted_files = unzip_response_content(response_content)

for file_name, file_content in extracted_files.items():
    file_stem = Path(file_name).stem

    if file_name.startswith("Metadata_"):
        write_response_content_as_csv_to_path(
            file_content,
            GDP_METADATA_RAW_DIR,
            file_stem,
        )
    else:
        write_response_content_as_csv_to_path(
            file_content,
            GDP_DATA_RAW_DIR,
            "world_bank_gdp_per_capita",
        )
