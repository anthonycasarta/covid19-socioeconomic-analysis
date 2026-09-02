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
# MAGIC ## Create a Temporary View consisting of only healthcare related data by country

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace temp view owid_country_healthcare as
# MAGIC (
# MAGIC     select
# MAGIC         country,
# MAGIC         date,
# MAGIC         population_density,
# MAGIC         median_age,
# MAGIC         life_expectancy,
# MAGIC         diabetes_prevalence,
# MAGIC         handwashing_facilities,
# MAGIC         hospital_beds_per_thousand,
# MAGIC         human_development_index
# MAGIC     from covid_owid_raw
# MAGIC );
# MAGIC
# MAGIC select
# MAGIC     *
# MAGIC from 
# MAGIC     owid_country_healthcare
# MAGIC limit
# MAGIC     10
# MAGIC ;

# COMMAND ----------

# MAGIC %md
# MAGIC # Analyze core metric table
# MAGIC ---------
# MAGIC
# MAGIC ### Overview of take aways:
# MAGIC
# MAGIC 1. There aren't any values that are less than or equal to 0. However, the assumption cannot be made that a null value is actually a value of 0. Considering all other values that come from the original dataset have null values as missing data, that will be the assumption for these null values. That is to say, the null values must be imputed or dropped as has been the case with the other data from the originating dataset.
# MAGIC
# MAGIC 2. Some countries are reused or grouped with other countries. Where possible, each row will only consist of one country. Exclude countries: Asia excl. China; World; World excl. China; World excl. China, South Korea; World excl. China, South Korea, Japan and Singapore; Winter Olympics 2022; Summer Olympics 2020; Low-income countries; Lower-middle-income countries; High-income countries; European Union (27).
# MAGIC
# MAGIC <div>
# MAGIC <strong> Note: </strong>
# MAGIC </div>
# MAGIC The countries grouped, such as: Low-income countries, Lower-middle-income countries, and so on can perhaps be used in the future once we categorize the countries as falling into one of these groups. That is to say, we can analyze how our classifications compare to the ones that the dataset includes.
# MAGIC
# MAGIC 3. The features: Human Development Index and Handwashing Facilities will be dropped because of a high null rate. Population Density, Median Age, Life Expectancy, Diabetes Prevalence, and Hospital Beds Per Thousand will be kept and records that are null for these features will be dropped.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Find Minimum Values of Numeric Columns
# MAGIC ----
# MAGIC
# MAGIC - There aren't any values that are less than or equal to 0. However, the assumption cannot be made that a null value is actually a value of 0. Considering all other values that come from the original dataset have null values as missing data, that will be the assumption for these null values. That is to say, the null values must be imputed or dropped as has been the case with the other data from the originating dataset.

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     min(population_density) as min_population_density,
# MAGIC     min(median_age) as min_median_age,
# MAGIC     min(life_expectancy) as min_life_expectancy,
# MAGIC     min(diabetes_prevalence) as min_diabetes_prevalence,
# MAGIC     min(handwashing_facilities) as min_handwashing_facilities,
# MAGIC     min(hospital_beds_per_thousand) as min_hospital_beds_per_thousand,
# MAGIC     min(human_development_index) as min_human_development_index
# MAGIC from
# MAGIC     owid_country_healthcare
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
# MAGIC     owid_country_healthcare
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
        owid_healthcare_nulls
    as 
    (
        select
            date_trunc('MONTH', date) as month,
            case when population_density is null then 1 else 0 end as population_density_nulls,
            case when median_age is null then 1 else 0 end as median_age_nulls,
            case when life_expectancy is null then 1 else 0 end as life_expectancy_nulls,
            case when diabetes_prevalence is null then 1 else 0 end as diabetes_prevalence_nulls,
            case when handwashing_facilities is null then 1 else 0 end as handwashing_facilities_nulls,
            case when hospital_beds_per_thousand is null then 1 else 0 end as hospital_beds_per_thousand_nulls,
            case when human_development_index is null then 1 else 0 end as human_development_index_nulls
        from
            owid_country_healthcare
    )
    select
        month,
        avg(population_density_nulls) as population_density_null_rate,
        avg(median_age_nulls) as median_age_null_rate,
        avg(life_expectancy_nulls) as life_expectancy_null_rate,
        avg(diabetes_prevalence_nulls) as diabetes_prevalence_null_rate,
        avg(handwashing_facilities_nulls) as handwashing_facilities_null_rate,
        avg(hospital_beds_per_thousand_nulls) as hospital_beds_per_thousand_null_rate,
        avg(human_development_index_nulls) as human_development_index_null_rate
    from
        owid_healthcare_nulls
    group by
        month
    order by
        month
    ;
    '''
)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Heatmap of Monthly Null Rates
# MAGIC ----
# MAGIC
# MAGIC - Human Development Index has a null rate of 1 for all months, so that feature should be dropped.
# MAGIC - The Handwashing Facilities feature may or may not be at a rate of about 0.5. It depends on how may countries are affected by this null rate. That is to say, if most countries are at a rate of around 0.5, then the feature will be dropped. If most countries have a null rate below that, then certain rows will be dropped.
# MAGIC - The features: Population Density, Median Age, Life Expenctancy, Diabetes Prevalence, and Hospital Beds Per Thousand will be kept since they all are less than or equal to a 0.3 null rate.

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
    title="OWID Healthcare Null Rates by Month",
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

# MAGIC %md
# MAGIC #### Null Rates by Country

# COMMAND ----------


null_rates_by_country_df = spark.sql(
    '''
    with
        owid_healthcare_nulls
    as 
    (
        select
            country,
            case when population_density is null then 1 else 0 end as population_density_nulls,
            case when median_age is null then 1 else 0 end as median_age_nulls,
            case when life_expectancy is null then 1 else 0 end as life_expectancy_nulls,
            case when diabetes_prevalence is null then 1 else 0 end as diabetes_prevalence_nulls,
            case when handwashing_facilities is null then 1 else 0 end as handwashing_facilities_nulls,
            case when hospital_beds_per_thousand is null then 1 else 0 end as hospital_beds_per_thousand_nulls,
            case when human_development_index is null then 1 else 0 end as human_development_index_nulls
        from
            owid_country_healthcare
        where
            country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China and South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
    )
    select
        country,
        avg(population_density_nulls) as population_density_null_rate,
        avg(median_age_nulls) as median_age_null_rate,
        avg(life_expectancy_nulls) as life_expectancy_null_rate,
        avg(diabetes_prevalence_nulls) as diabetes_prevalence_null_rate,
        avg(handwashing_facilities_nulls) as handwashing_facilities_null_rate,
        avg(hospital_beds_per_thousand_nulls) as hospital_beds_per_thousand_null_rate,
        avg(human_development_index_nulls) as human_development_index_null_rate
    from
        owid_healthcare_nulls
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
# MAGIC - For most countries the features: Population Density, Median Age, and Life Expectancy are not null.

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
    title="COVID-19 Null Rates by Country",
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
# MAGIC ### Check how many countries have a null rate of 1 for the features: Diabetes Prevalence and Hospital Beds Per Thousand
# MAGIC ----
# MAGIC
# MAGIC - There are 82 countries that have a null rate of 1 for the features: Diabetes Prevalence and Hospital Beds Per Thousand. That means that after removing the countries suggested in "List all distinct countries in the dataset", that would be 93 "countries" removed. Therefore, 262 - 93 = 169 total countries. 
# MAGIC
# MAGIC - Let's say that the actual total countries in the dataset is 262 - 11 = 251, then in removing the countries with a null rate of 1 for Diabetes Prevalence and Hospital Beds Per Thousand would leave 67% of the countries. 

# COMMAND ----------

# MAGIC %sql
# MAGIC with
# MAGIC         owid_healthcare_nulls
# MAGIC     as 
# MAGIC     (
# MAGIC         select
# MAGIC             country,
# MAGIC             case when population_density is null then 1 else 0 end as population_density_nulls,
# MAGIC             case when median_age is null then 1 else 0 end as median_age_nulls,
# MAGIC             case when life_expectancy is null then 1 else 0 end as life_expectancy_nulls,
# MAGIC             case when diabetes_prevalence is null then 1 else 0 end as diabetes_prevalence_nulls,
# MAGIC             case when handwashing_facilities is null then 1 else 0 end as handwashing_facilities_nulls,
# MAGIC             case when hospital_beds_per_thousand is null then 1 else 0 end as hospital_beds_per_thousand_nulls,
# MAGIC             case when human_development_index is null then 1 else 0 end as human_development_index_nulls
# MAGIC         from
# MAGIC             owid_country_healthcare
# MAGIC         where
# MAGIC             country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China and South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
# MAGIC     ),
# MAGIC         owid_healthcare_null_rate
# MAGIC     as
# MAGIC     (
# MAGIC     select
# MAGIC         country,
# MAGIC         avg(population_density_nulls) as population_density_null_rate,
# MAGIC         avg(median_age_nulls) as median_age_null_rate,
# MAGIC         avg(life_expectancy_nulls) as life_expectancy_null_rate,
# MAGIC         avg(diabetes_prevalence_nulls) as diabetes_prevalence_null_rate,
# MAGIC         avg(handwashing_facilities_nulls) as handwashing_facilities_null_rate,
# MAGIC         avg(hospital_beds_per_thousand_nulls) as hospital_beds_per_thousand_null_rate,
# MAGIC         avg(human_development_index_nulls) as human_development_index_null_rate
# MAGIC     from
# MAGIC         owid_healthcare_nulls
# MAGIC     group by
# MAGIC         country
# MAGIC     order by
# MAGIC         country
# MAGIC     )
# MAGIC     select
# MAGIC         country
# MAGIC     from
# MAGIC         owid_healthcare_null_rate
# MAGIC     where
# MAGIC         diabetes_prevalence_null_rate == 1
# MAGIC         or hospital_beds_per_thousand_null_rate == 1
# MAGIC     ;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Final Silver Covid Core Metrics Table
# MAGIC ---

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     country,
# MAGIC     date,
# MAGIC     population_density,
# MAGIC     median_age,
# MAGIC     life_expectancy,
# MAGIC     diabetes_prevalence,
# MAGIC     hospital_beds_per_thousand
# MAGIC from 
# MAGIC     owid_country_healthcare
# MAGIC where
# MAGIC     country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China and South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
# MAGIC     and country is not null
# MAGIC     and date is not null
# MAGIC     and population_density is not null
# MAGIC     and median_age is not null
# MAGIC     and life_expectancy is not null
# MAGIC     and diabetes_prevalence is not null
# MAGIC     and hospital_beds_per_thousand is not null
# MAGIC order by
# MAGIC     country,
# MAGIC     date
# MAGIC ;