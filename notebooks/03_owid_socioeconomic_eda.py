# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
import plotly.express as px

# COMMAND ----------

# MAGIC %md
# MAGIC ## Set Default Catalog and Schema

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog covid19_socioeconomic_analysis;
# MAGIC use schema bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create a Temporary View consisting of only scocioeconomic related data by country

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace temp view owid_country_socioeconomic as
# MAGIC (
# MAGIC     select
# MAGIC         country,
# MAGIC         date,
# MAGIC         gdp_per_capita,
# MAGIC         extreme_poverty
# MAGIC     from covid_owid_raw
# MAGIC );
# MAGIC
# MAGIC select
# MAGIC     *
# MAGIC from 
# MAGIC     owid_country_socioeconomic
# MAGIC limit
# MAGIC     10
# MAGIC ;

# COMMAND ----------

# MAGIC %md
# MAGIC # Analyze OWID Socioeconomic table
# MAGIC ---------
# MAGIC
# MAGIC ### Overview of take aways:

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Find Minimum Values of Numeric Columns
# MAGIC ----
# MAGIC
# MAGIC - Minimum values of 0 exist for numeric features. So, a null value does not mean 0, but must be imputed by some other method or dropped.

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     min(gdp_per_capita),
# MAGIC     min(extreme_poverty)
# MAGIC from
# MAGIC     owid_country_socioeconomic
# MAGIC ;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 2. List all distinct countries in the dataset
# MAGIC ---
# MAGIC
# MAGIC - Some countries are reused or grouped with other countries. Where possible, each row will only consist of one country. Exclude countries: Asia excl. China; World; World excl. China; World excl. China, South Korea; World excl. China, South Korea, Japan and Singapore; Winter Olympics 2022; Summer Olympics 2020; Low-income countries; Lower-middle-income countries; High-income countries; European Union (27).
# MAGIC
# MAGIC - The countries grouped, such as: Low-income countries, Lower-middle-income countries, and so on can perhaps be used in the future once we categorize the countries as falling into one of these groups. That is to say, we can analyze how our classifications compare to the ones that the dataset includes.

# COMMAND ----------

# MAGIC %sql
# MAGIC select distinct
# MAGIC     country
# MAGIC from
# MAGIC     owid_country_socioeconomic
# MAGIC order by
# MAGIC     country
# MAGIC ;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 3. Analyze null rates
# MAGIC ----
# MAGIC
# MAGIC <div>
# MAGIC <strong> Note: </strong>
# MAGIC </div>
# MAGIC Null rates are grouped by month and then by country.

# COMMAND ----------

null_rates_by_month_df = spark.sql(
    '''
    with 
        owid_socioeconomic_nulls
    as 
    (
        select
            date_trunc("MONTH", date) as month,
            case when gdp_per_capita is null then 1 else 0 end as gdp_per_capita_nulls,
            case when extreme_poverty is null then 1 else 0 end as extreme_poverty_nulls
        from 
            owid_country_socioeconomic
    )
    select
        month,
        avg(gdp_per_capita_nulls) as gdp_per_capita_null_rate,
        avg(extreme_poverty_nulls) as extreme_poverty_null_rate
    from owid_socioeconomic_nulls
    group by 
        month
    order by
        month
    ;
    '''
)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Heatmap of Null Rates by Month
# MAGIC ----
# MAGIC
# MAGIC - Null rates per month are fairly consistent at a null rate of about 0.2-0.3, however, all records after December 2022 will still be dropped as the core metric covid data is.

# COMMAND ----------

heatmap_data_by_month = (
    null_rates_by_month_df
    .orderBy("month")
    .toPandas()
    .set_index("month")
    .T
)

metric_names = heatmap_data_by_month.index.tolist()

# COMMAND ----------

figure = px.imshow(
    heatmap_data_by_month,
    aspect="auto",
    color_continuous_scale="RdYlGn_r",
    zmin=0,
    zmax=1,
    title="OWID Socioeconomic Null Rates by Month",
    labels={
        "x": "Month",
        "y": "Metric",
        "color": "Null rate",
    },
)

figure.update_yaxes(
    tickmode="array",
    tickvals=metric_names,
    ticktext=[
        metric.removesuffix("_null_rate")
        for metric in metric_names
    ],
    automargin=True,
)

figure.update_traces(
    xgap=1,
    ygap=1,
)

pixels_per_metric = 32
figure.update_layout(
    height=max(700, len(metric_names) * pixels_per_metric),
    margin={"l": 250},
    plot_bgcolor="white",
)

figure.update_coloraxes(
    colorbar_tickformat=".0%",
)

figure.show()

# COMMAND ----------

null_rates_by_country_df = spark.sql(
    '''
    with 
        owid_socioeconomic_nulls
    as 
    (
        select
            country,
            case when gdp_per_capita is null then 1 else 0 end as gdp_per_capita_nulls,
            case when extreme_poverty is null then 1 else 0 end as extreme_poverty_nulls
        from 
            owid_country_socioeconomic
        where
            country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China and South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
    )
    select
        country,
        avg(gdp_per_capita_nulls) as gdp_per_capita_null_rate,
        avg(extreme_poverty_nulls) as extreme_poverty_null_rate
    from owid_socioeconomic_nulls
    group by 
        country
    order by
        country
    ;
    '''
)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Heatmap of Null Rates by Country
# MAGIC ----
# MAGIC
# MAGIC - There are many countries that either have gdp per capita, extreme poverty, or both as a null rate of 1. These countries should be dropped.

# COMMAND ----------

heatmap_data_by_country = (
    null_rates_by_country_df
    .orderBy("country")
    .toPandas()
    .set_index("country")
    .T
)

metric_names = heatmap_data_by_country.index.tolist()
country_names = heatmap_data_by_country.columns.tolist()

# COMMAND ----------

figure = px.imshow(
    heatmap_data_by_country,
    aspect="auto",
    color_continuous_scale="RdYlGn_r",
    zmin=0,
    zmax=1,
    title="OWID Socioeconomic Null Rates by Country",
    labels={
        "x": "Country",
        "y": "Metric",
        "color": "Null rate",
    },
)

figure.update_yaxes(
    tickmode="array",
    tickvals=metric_names,
    ticktext=[
        metric.removesuffix("_null_rate")
        for metric in metric_names
    ],
    automargin=True,
)

figure.update_traces(
    xgap=1,
    ygap=1,
)

pixels_per_metric = 32
figure.update_layout(
    height=max(700, len(metric_names) * pixels_per_metric),
    width=max(1200, len(country_names) * 25),
    margin={"l": 250},
    plot_bgcolor="white",
)

figure.update_coloraxes(
    colorbar_tickformat=".0%",
)

figure.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Final Silver OWID Socioeconomic Metrics Table
# MAGIC ----

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     country,
# MAGIC     date,
# MAGIC     gdp_per_capita,
# MAGIC     extreme_poverty
# MAGIC from 
# MAGIC     owid_country_socioeconomic
# MAGIC where
# MAGIC     date < '2023-01-01'
# MAGIC     and country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China and South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
# MAGIC     and country is not null
# MAGIC     and gdp_per_capita is not null
# MAGIC     and extreme_poverty is not null
# MAGIC order by
# MAGIC     country,
# MAGIC     date
# MAGIC ;