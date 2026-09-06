# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog covid19_socioeconomic_analysis;

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
        gdp_per_capita > 0
    ;
    '''
)

# COMMAND ----------

country_gdp.groupBy("country").count().where("count > 1").show()

# COMMAND ----------

assembler = VectorAssembler(
    inputCols=["log_gdp_per_capita"],
    outputCol="features",
)

country_gdp_features = assembler.transform(country_gdp)

# COMMAND ----------

model = KMeans(
    k=3,
    seed=42,
    featuresCol="features",
    predictionCol="cluster_id",
).fit(country_gdp_features)