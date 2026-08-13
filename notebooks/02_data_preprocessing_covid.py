# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC ##Review Covid data

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM covid19_socioeconomic_analysis.bronze.covid_owid_raw
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE TABLE EXTENDED covid19_socioeconomic_analysis.bronze.covid_owid_raw;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Get record count of Covid data
# MAGIC SELECT COUNT(*) AS record_count
# MAGIC FROM covid19_socioeconomic_analysis.bronze.covid_owid_raw;

# COMMAND ----------

# DBTITLE 1,Calculate null rates for all columns

# Calculate null rates for all columns
from pyspark.sql.functions import col, count, when, round as spark_round

# Read the table
df = spark.table("covid19_socioeconomic_analysis.bronze.covid_owid_raw")

# Calculate null counts for all columns
total_count = df.count()
null_stats = df.select([
    count(when(col(c).isNull(), c)).alias(c) 
    for c in df.columns
]).collect()[0]

# Convert to a DataFrame for display
from pyspark.sql import Row
results = [
    Row(
        column_name=c,
        null_count=null_stats[c],
        total_count=total_count,
        null_rate=round(null_stats[c] / total_count, 4)
    )
    for c in df.columns
]

null_rate_df = spark.createDataFrame(results).orderBy("null_rate", ascending=False)
display(null_rate_df)

# COMMAND ----------

from pyspark.sql.functions import col

acceptable_null_rate_columns = [
    row.column_name
    for row in null_rate_df.filter(
        (col("null_rate") <= 0.4) & (~col("column_name").rlike("_rescued_data"))
    ).collect()
]

display(acceptable_null_rate_columns)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM covid19_socioeconomic_analysis.silver.covid_daily
# MAGIC LIMIT 50;