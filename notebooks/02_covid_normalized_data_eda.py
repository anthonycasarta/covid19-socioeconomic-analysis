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
# MAGIC USE CATALOG covid19_socioeconomic_analysis;
# MAGIC USE SCHEMA bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create a Temporary View consisting of only normalized metric data

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace temp view covid_normalized_metrics as
# MAGIC (
# MAGIC select
# MAGIC     country,
# MAGIC     date,
# MAGIC     new_cases_smoothed,
# MAGIC     total_cases_per_million,
# MAGIC     new_cases_per_million,
# MAGIC     new_cases_smoothed_per_million,
# MAGIC     new_deaths_smoothed,
# MAGIC     total_deaths_per_million,
# MAGIC     new_deaths_per_million,
# MAGIC     new_deaths_smoothed_per_million,
# MAGIC     total_tests_per_thousand,
# MAGIC     new_tests_per_thousand,
# MAGIC     new_tests_smoothed,
# MAGIC     new_tests_smoothed_per_thousand,
# MAGIC     total_vaccinations_per_hundred,
# MAGIC     people_vaccinated_per_hundred,
# MAGIC     people_fully_vaccinated_per_hundred,
# MAGIC     total_boosters_per_hundred,
# MAGIC     new_vaccinations_smoothed,
# MAGIC     new_vaccinations_smoothed_per_million,
# MAGIC     new_people_vaccinated_smoothed,
# MAGIC     new_people_vaccinated_smoothed_per_hundred,
# MAGIC     hosp_patients_per_million,
# MAGIC     weekly_hosp_admissions_per_million,
# MAGIC     icu_patients_per_million,
# MAGIC     weekly_icu_admissions_per_million,
# MAGIC     excess_mortality_cumulative_per_million
# MAGIC from covid_owid_raw
# MAGIC );
# MAGIC
# MAGIC select
# MAGIC     *
# MAGIC from 
# MAGIC     covid_normalized_metrics
# MAGIC limit
# MAGIC     10
# MAGIC ;

# COMMAND ----------

# MAGIC %md
# MAGIC # Analyze core normalized metric table
# MAGIC ---------
# MAGIC
# MAGIC ### Overview of take aways:
# MAGIC
# MAGIC 1. The minimum values of the numeric columns are less than or equal to the value 0. That means that nulls cannot represent 0 values, confirming that null values are missing values and cannot be replaced with the value 0.
# MAGIC
# MAGIC 2. Some countries are reused or grouped with other countries. Where possible, each row will only consist of one country. Exclude countries: Asia excl. China; World; World excl. China; World excl. China, South Korea; World excl. China, South Korea, Japan and Singapore; Winter Olympics 2022; Summer Olympics 2020; Low-income countries; Lower-middle-income countries; High-income countries; European Union (27).
# MAGIC
# MAGIC <div>
# MAGIC <strong> Note: </strong>
# MAGIC </div>
# MAGIC The countries grouped, such as: Low-income countries, Lower-middle-income countries, and so on can perhaps be used in the future once we categorize the countries as falling into one of these groups. That is to say, we can analyze how our classifications compare to the ones that the dataset includes.
# MAGIC
# MAGIC 3. Null rates per month are fairly consistent, however, all records after December 2022 will still be dropped as the core metric covid data is. Again, like covid core metrics, most countries have null values for the same features. Therefore, dropping records with null values will significantly reduce the number of countries in the dataset. This is not an option.

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Find Minimum Values of Numeric Columns
# MAGIC ----
# MAGIC
# MAGIC - The minimum values of the numeric columns are less than or equal to the value 0. That means that nulls cannot represent 0 values, confirming that null values are missing values and cannot be replaced with the value 0.

# COMMAND ----------

# MAGIC %sql
# MAGIC select 
# MAGIC     min(new_cases_smoothed) as min_new_cases_smoothed,
# MAGIC     min(total_cases_per_million) as min_total_cases_per_million,
# MAGIC     min(new_cases_per_million) as min_new_cases_per_million,
# MAGIC     min(new_cases_smoothed_per_million) as min_new_cases_smoothed_per_million,
# MAGIC     min(new_deaths_smoothed) as min_new_deaths_smoothed,
# MAGIC     min(total_deaths_per_million) as min_total_deaths_per_million,
# MAGIC     min(new_deaths_per_million) as min_new_deaths_per_million,
# MAGIC     min(new_deaths_smoothed_per_million) as min_new_deaths_smoothed_per_million,
# MAGIC     min(total_tests_per_thousand) as min_total_tests_per_thousand,
# MAGIC     min(new_tests_per_thousand) as min_new_tests_per_thousand,
# MAGIC     min(new_tests_smoothed) as min_new_tests_smoothed,
# MAGIC     min(new_tests_smoothed_per_thousand) as min_new_tests_smoothed_per_thousand,
# MAGIC     min(total_vaccinations_per_hundred) as min_total_vaccinations_per_hundred,
# MAGIC     min(people_vaccinated_per_hundred) as min_people_vaccinated_per_hundred,
# MAGIC     min(people_fully_vaccinated_per_hundred) as min_people_fully_vaccinated_per_hundred,
# MAGIC     min(total_boosters_per_hundred) as min_total_boosters_per_hundred,
# MAGIC     min(new_vaccinations_smoothed) as min_new_vaccinations_smoothed,
# MAGIC     min(new_vaccinations_smoothed_per_million) as min_new_vaccinations_smoothed_per_million,
# MAGIC     min(new_people_vaccinated_smoothed) as min_new_people_vaccinated_smoothed,
# MAGIC     min(new_people_vaccinated_smoothed_per_hundred) as min_new_people_vaccinated_smoothed_per_hundred,
# MAGIC     min(hosp_patients_per_million) as min_hosp_patients_per_million,
# MAGIC     min(weekly_hosp_admissions_per_million) as min_weekly_hosp_admissions_per_million,
# MAGIC     min(icu_patients_per_million) as min_icu_patients_per_million,
# MAGIC     min(weekly_icu_admissions_per_million) as min_weekly_icu_admissions_per_million,
# MAGIC     min(excess_mortality_cumulative_per_million) as min_excess_mortality_cumulative_per_million
# MAGIC from covid_normalized_metrics
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
# MAGIC     covid_normalized_metrics
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

# MAGIC %md
# MAGIC #### Monthly Null Rates

# COMMAND ----------

null_rates_by_month_df = spark.sql(
'''
with
    covid_normalized_metric_nulls
as
(
    select
        date_trunc("MONTH", date) as month,
        case when new_cases_smoothed is null then 1 else 0 end as new_cases_smoothed_nulls,
        case when total_cases_per_million is null then 1 else 0 end as total_cases_per_million_nulls,
        case when new_cases_per_million is null then 1 else 0 end as new_cases_per_million_nulls,
        case when new_deaths_smoothed is null then 1 else 0 end as new_deaths_smoothed_nulls,
        case when total_deaths_per_million is null then 1 else 0 end as total_deaths_per_million_nulls,
        case when new_deaths_per_million is null then 1 else 0 end as new_deaths_per_million_nulls,
        case when new_deaths_smoothed_per_million is null then 1 else 0 end as new_deaths_smoothed_per_million_nulls,
        case when total_tests_per_thousand is null then 1 else 0 end as total_tests_per_thousand_nulls,
        case when new_tests_per_thousand is null then 1 else 0 end as new_tests_per_thousand_nulls,
        case when new_tests_smoothed is null then 1 else 0 end as new_tests_smoothed_nulls,
        case when new_tests_smoothed_per_thousand is null then 1 else 0 end as new_tests_smoothed_per_thousand_nulls,
        case when total_vaccinations_per_hundred is null then 1 else 0 end as total_vaccinations_per_hundred_nulls,
        case when people_vaccinated_per_hundred is null then 1 else 0 end as people_vaccinated_per_hundred_nulls,
        case when people_fully_vaccinated_per_hundred is null then 1 else 0 end as people_fully_vaccinated_per_hundred_nulls,
        case when total_boosters_per_hundred is null then 1 else 0 end as total_boosters_per_hundred_nulls,
        case when new_vaccinations_smoothed is null then 1 else 0 end as new_vaccinations_smoothed_nulls,
        case when new_vaccinations_smoothed_per_million is null then 1 else 0 end as new_vaccinations_smoothed_per_million_nulls,
        case when new_people_vaccinated_smoothed is null then 1 else 0 end as new_people_vaccinated_smoothed_nulls,
        case when new_people_vaccinated_smoothed_per_hundred is null then 1 else 0 end as new_people_vaccinated_smoothed_per_hundred_nulls,
        case when hosp_patients_per_million is null then 1 else 0 end as hosp_patients_per_million_nulls,
        case when weekly_hosp_admissions_per_million is null then 1 else 0 end as weekly_hosp_admissions_per_million_nulls,
        case when icu_patients_per_million is null then 1 else 0 end as icu_patients_per_million_nulls,
        case when weekly_icu_admissions_per_million is null then 1 else 0 end as weekly_icu_admissions_per_million_nulls,
        case when excess_mortality_cumulative_per_million is null then 1 else 0 end as excess_mortality_cumulative_per_million_nulls
    from
        covid_normalized_metrics
)
select 
    month,
    avg(new_cases_smoothed_nulls) as new_cases_smoothed_null_rate,
    avg(total_cases_per_million_nulls) as total_cases_per_million_null_rate,
    avg(new_cases_per_million_nulls) as new_cases_per_million_null_rate,
    avg(new_deaths_smoothed_nulls) as new_deaths_smoothed_null_rate,
    avg(total_deaths_per_million_nulls) as total_deaths_per_million_null_rate,
    avg(new_deaths_per_million_nulls) as new_deaths_per_million_null_rate,
    avg(new_deaths_smoothed_per_million_nulls) as new_deaths_smoothed_per_million_null_rate,
    avg(total_tests_per_thousand_nulls) as total_tests_per_thousand_null_rate,
    avg(new_tests_per_thousand_nulls) as new_tests_per_thousand_null_rate,
    avg(new_tests_smoothed_nulls) as new_tests_smoothed_null_rate,
    avg(new_tests_smoothed_per_thousand_nulls) as new_tests_smoothed_per_thousand_null_rate,
    avg(total_vaccinations_per_hundred_nulls) as total_vaccinations_per_hundred_null_rate,
    avg(people_vaccinated_per_hundred_nulls) as people_vaccinated_per_hundred_null_rate,
    avg(people_fully_vaccinated_per_hundred_nulls) as people_fully_vaccinated_per_hundred_null_rate,
    avg(total_boosters_per_hundred_nulls) as total_boosters_per_hundred_null_rate,
    avg(new_vaccinations_smoothed_nulls) as new_vaccinations_smoothed_null_rate,
    avg(new_vaccinations_smoothed_per_million_nulls) as new_vaccinations_smoothed_per_million_null_rate,
    avg(new_people_vaccinated_smoothed_nulls) as new_people_vaccinated_smoothed_null_rate,
    avg(new_people_vaccinated_smoothed_per_hundred_nulls) as new_people_vaccinated_smoothed_per_hundred_null_rate,
    avg(hosp_patients_per_million_nulls) as hosp_patients_per_million_null_rate,
    avg(weekly_hosp_admissions_per_million_nulls) as weekly_hosp_admissions_per_million_null_rate,
    avg(icu_patients_per_million_nulls) as icu_patients_per_million_null_rate,
    avg(weekly_icu_admissions_per_million_nulls) as weekly_icu_admissions_per_million_null_rate,
    avg(excess_mortality_cumulative_per_million_nulls) as excess_mortality_cumulative_per_million_null_rate
from 
    covid_normalized_metric_nulls
group by 
    month
order by 
    month
;
''')

# COMMAND ----------

# MAGIC %md
# MAGIC #### Heatmap of Null Rates by Month
# MAGIC ----
# MAGIC
# MAGIC - Null rates per month are fairly consistent, however, all records after December 2022 will still be dropped as the core metric covid data is.

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
    title="COVID-19 Null Rates by Month",
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
    covid_normalized_metric_nulls
as
(
    select
        country,
        case when new_cases_smoothed is null then 1 else 0 end as new_cases_smoothed_nulls,
        case when total_cases_per_million is null then 1 else 0 end as total_cases_per_million_nulls,
        case when new_cases_per_million is null then 1 else 0 end as new_cases_per_million_nulls,
        case when new_deaths_smoothed is null then 1 else 0 end as new_deaths_smoothed_nulls,
        case when total_deaths_per_million is null then 1 else 0 end as total_deaths_per_million_nulls,
        case when new_deaths_per_million is null then 1 else 0 end as new_deaths_per_million_nulls,
        case when new_deaths_smoothed_per_million is null then 1 else 0 end as new_deaths_smoothed_per_million_nulls,
        case when total_tests_per_thousand is null then 1 else 0 end as total_tests_per_thousand_nulls,
        case when new_tests_per_thousand is null then 1 else 0 end as new_tests_per_thousand_nulls,
        case when new_tests_smoothed is null then 1 else 0 end as new_tests_smoothed_nulls,
        case when new_tests_smoothed_per_thousand is null then 1 else 0 end as new_tests_smoothed_per_thousand_nulls,
        case when total_vaccinations_per_hundred is null then 1 else 0 end as total_vaccinations_per_hundred_nulls,
        case when people_vaccinated_per_hundred is null then 1 else 0 end as people_vaccinated_per_hundred_nulls,
        case when people_fully_vaccinated_per_hundred is null then 1 else 0 end as people_fully_vaccinated_per_hundred_nulls,
        case when total_boosters_per_hundred is null then 1 else 0 end as total_boosters_per_hundred_nulls,
        case when new_vaccinations_smoothed is null then 1 else 0 end as new_vaccinations_smoothed_nulls,
        case when new_vaccinations_smoothed_per_million is null then 1 else 0 end as new_vaccinations_smoothed_per_million_nulls,
        case when new_people_vaccinated_smoothed is null then 1 else 0 end as new_people_vaccinated_smoothed_nulls,
        case when new_people_vaccinated_smoothed_per_hundred is null then 1 else 0 end as new_people_vaccinated_smoothed_per_hundred_nulls,
        case when hosp_patients_per_million is null then 1 else 0 end as hosp_patients_per_million_nulls,
        case when weekly_hosp_admissions_per_million is null then 1 else 0 end as weekly_hosp_admissions_per_million_nulls,
        case when icu_patients_per_million is null then 1 else 0 end as icu_patients_per_million_nulls,
        case when weekly_icu_admissions_per_million is null then 1 else 0 end as weekly_icu_admissions_per_million_nulls,
        case when excess_mortality_cumulative_per_million is null then 1 else 0 end as excess_mortality_cumulative_per_million_nulls
    from
        covid_normalized_metrics
)
select 
    country,
    avg(new_cases_smoothed_nulls) as new_cases_smoothed_null_rate,
    avg(total_cases_per_million_nulls) as total_cases_per_million_null_rate,
    avg(new_cases_per_million_nulls) as new_cases_per_million_null_rate,
    avg(new_deaths_smoothed_nulls) as new_deaths_smoothed_null_rate,
    avg(total_deaths_per_million_nulls) as total_deaths_per_million_null_rate,
    avg(new_deaths_per_million_nulls) as new_deaths_per_million_null_rate,
    avg(new_deaths_smoothed_per_million_nulls) as new_deaths_smoothed_per_million_null_rate,
    avg(total_tests_per_thousand_nulls) as total_tests_per_thousand_null_rate,
    avg(new_tests_per_thousand_nulls) as new_tests_per_thousand_null_rate,
    avg(new_tests_smoothed_nulls) as new_tests_smoothed_null_rate,
    avg(new_tests_smoothed_per_thousand_nulls) as new_tests_smoothed_per_thousand_null_rate,
    avg(total_vaccinations_per_hundred_nulls) as total_vaccinations_per_hundred_null_rate,
    avg(people_vaccinated_per_hundred_nulls) as people_vaccinated_per_hundred_null_rate,
    avg(people_fully_vaccinated_per_hundred_nulls) as people_fully_vaccinated_per_hundred_null_rate,
    avg(total_boosters_per_hundred_nulls) as total_boosters_per_hundred_null_rate,
    avg(new_vaccinations_smoothed_nulls) as new_vaccinations_smoothed_null_rate,
    avg(new_vaccinations_smoothed_per_million_nulls) as new_vaccinations_smoothed_per_million_null_rate,
    avg(new_people_vaccinated_smoothed_nulls) as new_people_vaccinated_smoothed_null_rate,
    avg(new_people_vaccinated_smoothed_per_hundred_nulls) as new_people_vaccinated_smoothed_per_hundred_null_rate,
    avg(hosp_patients_per_million_nulls) as hosp_patients_per_million_null_rate,
    avg(weekly_hosp_admissions_per_million_nulls) as weekly_hosp_admissions_per_million_null_rate,
    avg(icu_patients_per_million_nulls) as icu_patients_per_million_null_rate,
    avg(weekly_icu_admissions_per_million_nulls) as weekly_icu_admissions_per_million_null_rate,
    avg(excess_mortality_cumulative_per_million_nulls) as excess_mortality_cumulative_per_million_null_rate
from 
    covid_normalized_metric_nulls
group by 
    country
order by 
    country
;
''')

# COMMAND ----------

# MAGIC %md
# MAGIC #### Heatmap of Null Rates by Country
# MAGIC ----
# MAGIC
# MAGIC - Again, like covid core metrics, most countries have null values for the same features. Therefore, dropping records with null values will significantly reduce the number of countries in the dataset. This is not an option.

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
# MAGIC ### Final Silver Covid Core Metrics Table
# MAGIC ----

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     country,
# MAGIC     date,
# MAGIC     new_cases_per_million,
# MAGIC     new_cases_smoothed,
# MAGIC     total_cases_per_million,
# MAGIC     new_deaths_per_million,
# MAGIC     new_deaths_smoothed,
# MAGIC     new_deaths_smoothed_per_million,
# MAGIC     total_deaths_per_million
# MAGIC from 
# MAGIC     covid_owid_raw
# MAGIC where
# MAGIC     date < '2023-01-01'
# MAGIC     and country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China, South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
# MAGIC     and country is not null
# MAGIC     and new_cases_per_million is not null
# MAGIC     and new_cases_smoothed is not null
# MAGIC     and total_cases_per_million is not null
# MAGIC     and new_deaths_per_million is not null
# MAGIC     and new_deaths_smoothed is not null
# MAGIC     and new_deaths_smoothed_per_million is not null
# MAGIC     and total_deaths_per_million is not null
# MAGIC order by
# MAGIC     country,
# MAGIC     date
# MAGIC ;