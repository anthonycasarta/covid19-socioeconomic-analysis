# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog covid19_socioeconomic_analysis;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     YEAR(TRY_CAST(date AS DATE)) AS observation_year,
# MAGIC     COUNT(DISTINCT country) AS countries,
# MAGIC     COUNT(DISTINCT CASE
# MAGIC         WHEN TRY_CAST(gdp_per_capita AS DOUBLE) > 0
# MAGIC         THEN country
# MAGIC     END) AS countries_with_gdp
# MAGIC FROM silver.owid_socioeconomic_daily
# MAGIC GROUP BY observation_year
# MAGIC ORDER BY observation_year;

# COMMAND ----------

country_gdp = spark.sql(
    '''
    select distinct
        country,
        gdp_per_capita,
        LN(gdp_per_capita) as log_gdp_per_capita
    from 
        silver.owid_socioeconomic_daily
    where 
        year(date) = 2020
        and gdp_per_capita > 0
    ;
    '''
)

# COMMAND ----------

display(
    country_gdp
    .groupBy("country")
    .count()
    .where("count > 1")
)

# COMMAND ----------

assembler = VectorAssembler(
    inputCols=["log_gdp_per_capita"],
    outputCol="features",
)

country_gdp_features = assembler.transform(country_gdp)

# COMMAND ----------

display(country_gdp_features)

# COMMAND ----------

model = KMeans(
    k=3,
    seed=42,
    featuresCol="features",
    predictionCol="cluster_id",
).fit(country_gdp_features)

# COMMAND ----------

clustered_countries = model.transform(country_gdp_features)

display(
    clustered_countries
    .select(
        "country",
        "gdp_per_capita",
        "cluster_id",
    )
    .orderBy("gdp_per_capita")
)