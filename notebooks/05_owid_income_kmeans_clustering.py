# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.sql import functions as F
import math

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

# COMMAND ----------

log_centers = [
    float(center[0])
    for center in model.clusterCenters()
]

cluster_centers = [
    (
        cluster_id,
        log_center,
        math.exp(log_center),
    )
    for cluster_id, log_center in enumerate(log_centers)
]

cluster_centers

# COMMAND ----------

ordered_centers = sorted(
    cluster_centers,
    key=lambda item: item[2],
)

income_labels = ["Low-GDP", "Middle-GDP", "High-GDP"]

cluster_mapping_rows = [
    (
        int(cluster_id),
        income_labels[position],
        float(log_center),
        float(gdp_center),
    )
    for position, (
        cluster_id,
        log_center,
        gdp_center,
    ) in enumerate(ordered_centers)
]

cluster_mapping = spark.createDataFrame(
    cluster_mapping_rows,
    """
    cluster_id INT,
    gdp_cluster STRING,
    cluster_center_log_gdp DOUBLE,
    cluster_center_gdp DOUBLE
    """,
)

display(cluster_mapping.orderBy("cluster_center_gdp"))

# COMMAND ----------

classified_countries = (
    clustered_countries
    .join(
        F.broadcast(cluster_mapping),
        on="cluster_id",
        how="inner",
    )
)

display(
    classified_countries
    .select(
        "country",
        "gdp_per_capita",
        "cluster_id",
        "gdp_cluster",
        "cluster_center_gdp",
    )
    .orderBy(F.col("gdp_per_capita").cast("double"))
)



# COMMAND ----------

display(
    classified_countries
    .groupBy(
        "gdp_cluster",
        "cluster_center_gdp",
    )
    .agg(
        F.count("*").alias("country_count"),
        F.min("gdp_per_capita").alias("minimum_gdp"),
        F.avg("gdp_per_capita").alias("average_gdp"),
        F.max("gdp_per_capita").alias("maximum_gdp"),
    )
    .orderBy("cluster_center_gdp")
)

# COMMAND ----------

from pyspark.ml.evaluation import ClusteringEvaluator

evaluator = ClusteringEvaluator(
    featuresCol="features",
    predictionCol="cluster_id",
    metricName="silhouette",
    distanceMeasure="squaredEuclidean",
)

silhouette_score = evaluator.evaluate(classified_countries)

print(f"Silhouette score: {silhouette_score:.4f}")

# COMMAND ----------

gdp_classifications = (
    classified_countries
    .select(
        "country",
        F.col("gdp_per_capita").cast("double").alias("gdp_per_capita"),
        "log_gdp_per_capita",
        "cluster_id",
        "gdp_cluster",
        "cluster_center_log_gdp",
        "cluster_center_gdp",
    )
    .withColumn("model_k", F.lit(3))
    .withColumn("model_seed", F.lit(42))
)

# COMMAND ----------

gdp_classifications.write.mode(
    "overwrite"
).option(
    "overwriteSchema",
    "true",
).saveAsTable(
    "covid19_socioeconomic_analysis.gold.owid_gdp_classification"
)