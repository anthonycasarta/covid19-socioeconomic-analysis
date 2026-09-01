# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
import plotly.express as px

# COMMAND ----------

# MAGIC %md
# MAGIC ## Set Catalog and Schema

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG covid19_socioeconomic_analysis;
# MAGIC USE SCHEMA bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Initial look at OWID Covid-19 raw data

# COMMAND ----------

# DBTITLE 1,Binary null indicators for all columns
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   covid_owid_raw
# MAGIC LIMIT
# MAGIC     10
# MAGIC ;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create a Temporary View consisting of only core metric data

# COMMAND ----------

# MAGIC %sql
# MAGIC -- The covid_core_metrics table will be created in the pipeline
# MAGIC -- For now, this will remain a temporary view so as to not preemptively create the table
# MAGIC create or replace temp view 
# MAGIC     covid_core_metrics 
# MAGIC as
# MAGIC (
# MAGIC select
# MAGIC     country,
# MAGIC     date,
# MAGIC     code,
# MAGIC     continent,
# MAGIC     population,
# MAGIC     total_cases,
# MAGIC     new_cases,
# MAGIC     total_deaths,
# MAGIC     new_deaths,
# MAGIC     total_tests,
# MAGIC     new_tests,
# MAGIC     positive_rate,
# MAGIC     tests_per_case,
# MAGIC     total_vaccinations,
# MAGIC     people_vaccinated,
# MAGIC     people_fully_vaccinated,
# MAGIC     total_boosters,
# MAGIC     new_vaccinations,
# MAGIC     hosp_patients,
# MAGIC     weekly_hosp_admissions,
# MAGIC     icu_patients,
# MAGIC     weekly_icu_admissions,
# MAGIC     excess_mortality,
# MAGIC     excess_mortality_cumulative,
# MAGIC     excess_mortality_cumulative_absolute,
# MAGIC     stringency_index,
# MAGIC     reproduction_rate
# MAGIC from 
# MAGIC     covid_owid_raw
# MAGIC );
# MAGIC
# MAGIC select
# MAGIC     *
# MAGIC from
# MAGIC     covid_core_metrics
# MAGIC limit
# MAGIC     10
# MAGIC ;

# COMMAND ----------

# MAGIC %md
# MAGIC # Analyze core metric table
# MAGIC ---------
# MAGIC
# MAGIC ### Overview of take aways:
# MAGIC 1. The minimum values of the numeric columns are less than or equal to the value 0. That means that nulls cannot represent 0 values, confirming that null values are missing values and cannot be replaced with the value 0.
# MAGIC
# MAGIC 2. Some countries are reused or grouped with other countries. Where possible, each row will only consist of one country. Exclude countries: Asia excl. China; World; World excl. China; World excl. China, South Korea; World excl. China, South Korea, Japan and Singapore; Winter Olympics 2022; Summer Olympics 2020; Low-income countries; Lower-middle-income countries; High-income countries; European Union (27).
# MAGIC
# MAGIC <div>
# MAGIC <strong> Note: </strong>
# MAGIC </div>
# MAGIC The countries grouped, such as: Low-income countries, Lower-middle-income countries, and so on can perhaps be used in the future once we categorize the countries as falling into one of these groups. That is to say, we can analyze how our classifications compare to the ones that the dataset includes. 
# MAGIC
# MAGIC 3. After January 2023 most of the data has a null rate of 0.8 or above. Given that most the of columns have such a high null rate at the start of that year, all rows with a date after December 2022 not be considered. The majority of countries are missing values in the same columns. So, dropping rows is not an option because it will significantly reduce the number of countries in the dataset.
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### 1. Find Minimum Values of Numeric Columns
# MAGIC ----
# MAGIC
# MAGIC - The minimum values of the numeric columns are less than or equal to the value 0. That means that nulls cannot represent 0 values, confirming that null values are missing values and cannot be replaced with the value 0.

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     min(total_cases) as total_cases_min_value,
# MAGIC     min(new_cases) as new_cases_min_value,
# MAGIC     min(total_deaths) as total_deaths_min_value,
# MAGIC     min(new_deaths) as new_deaths_min_value,
# MAGIC     min(total_tests) as total_tests_min_value,
# MAGIC     min(new_tests) as new_tests_min_value,
# MAGIC     min(positive_rate) as positive_rate_min_value,
# MAGIC     min(tests_per_case) as tests_per_case_min_value,
# MAGIC     min(total_vaccinations) as total_vaccinations_min_value,
# MAGIC     min(people_vaccinated) as people_vaccinated_min_value,
# MAGIC     min(people_fully_vaccinated) as people_fully_vaccinated_min_value,
# MAGIC     min(total_boosters) as total_boosters_min_value,
# MAGIC     min(new_vaccinations) as new_vaccinations_min_value,
# MAGIC     min(hosp_patients) as hosp_patients_min_value,
# MAGIC     min(weekly_hosp_admissions) as weekly_hosp_admissions_min_value,
# MAGIC     min(icu_patients) as icu_patients_min_value,
# MAGIC     min(weekly_icu_admissions) as weekly_icu_admissions_min_value,
# MAGIC     min(excess_mortality) as excess_mortality_min_value,
# MAGIC     min(excess_mortality_cumulative) as excess_mortality_cumulative_min_value,
# MAGIC     min(excess_mortality_cumulative_absolute) as excess_mortality_cumulative_absolute_min_value,
# MAGIC     min(stringency_index) as stringency_index_min_value,
# MAGIC     min(reproduction_rate) as reproduction_rate_min_value
# MAGIC from 
# MAGIC     covid_core_metrics;

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
# MAGIC     covid_core_metrics
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

# DBTITLE 1,Null analysis: Core metrics by date
null_rates_by_month_df = spark.sql('''
-- Null rates over time by month 
with 
    covid_core_nulls 
as
(
    select
        date_trunc('MONTH', date) as month,
        country,
        case when code is null then 1 else 0 end as code_null,
        case when continent is null then 1 else 0 end as continent_null,
        case when population is null then 1 else 0 end as population_null,
        case when total_cases is null then 1 else 0 end as total_cases_null,
        case when new_cases is null then 1 else 0 end as new_cases_null,
        case when total_deaths is null then 1 else 0 end as total_deaths_null,
        case when new_deaths is null then 1 else 0 end as new_deaths_null,
        case when total_tests is null then 1 else 0 end as total_tests_null,
        case when new_tests is null then 1 else 0 end as new_tests_null,
        case when positive_rate is null then 1 else 0 end as positive_rate_null,
        case when tests_per_case is null then 1 else 0 end as tests_per_case_null,
        case when total_vaccinations is null then 1 else 0 end as total_vaccinations_null,
        case when people_vaccinated is null then 1 else 0 end as people_vaccinated_null,
        case when people_fully_vaccinated is null then 1 else 0 end as people_fully_vaccinated_null,
        case when total_boosters is null then 1 else 0 end as total_boosters_null,
        case when new_vaccinations is null then 1 else 0 end as new_vaccinations_null,
        case when hosp_patients is null then 1 else 0 end as hosp_patients_null,
        case when weekly_hosp_admissions is null then 1 else 0 end as weekly_hosp_admissions_null,
        case when icu_patients is null then 1 else 0 end as icu_patients_null,
        case when weekly_icu_admissions is null then 1 else 0 end as weekly_icu_admissions_null,
        case when excess_mortality is null then 1 else 0 end as excess_mortality_null,
        case when excess_mortality_cumulative is null then 1 else 0 end as excess_mortality_cumulative_null,
        case when excess_mortality_cumulative_absolute is null then 1 else 0 end as excess_mortality_cumulative_absolute_null,
        case when stringency_index is null then 1 else 0 end as stringency_index_null,
        case when reproduction_rate is null then 1 else 0 end as reproduction_rate_null
    from 
        covid_core_metrics
    where
        country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China, South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
)
select
    month,
    avg(code_null) as code_null_rate,
    avg(continent_null) as continent_null_rate,
    avg(population_null) as population_null_rate,
    avg(total_cases_null) as total_cases_null_rate,
    avg(new_cases_null) as new_cases_null_rate,
    avg(total_deaths_null) as total_deaths_null_rate,
    avg(new_deaths_null) as new_deaths_null_rate,
    avg(total_tests_null) as total_tests_null_rate,
    avg(new_tests_null) as new_tests_null_rate,
    avg(positive_rate_null) as positive_rate_null_rate,
    avg(tests_per_case_null) as tests_per_case_null_rate,
    avg(total_vaccinations_null) as total_vaccinations_null_rate,
    avg(people_vaccinated_null) as people_vaccinated_null_rate,
    avg(people_fully_vaccinated_null) as people_fully_vaccinated_null_rate,
    avg(total_boosters_null) as total_boosters_null_rate,
    avg(new_vaccinations_null) as new_vaccinations_null_rate,
    avg(hosp_patients_null) as hosp_patients_null_rate,
    avg(weekly_hosp_admissions_null) as weekly_hosp_admissions_null_rate,
    avg(icu_patients_null) as icu_patients_null_rate,
    avg(weekly_icu_admissions_null) as weekly_icu_admissions_null_rate,
    avg(excess_mortality_null) as excess_mortality_null_rate,
    avg(excess_mortality_cumulative_null) as excess_mortality_cumulative_null_rate,
    avg(excess_mortality_cumulative_absolute_null) as excess_mortality_cumulative_absolute_null_rate,
    avg(stringency_index_null) as stringency_index_null_rate,
    avg(reproduction_rate_null) as reproduction_rate_null_rate
from 
    covid_core_nulls
group by
    month
order by
    month
;
''')

# COMMAND ----------

# MAGIC %md
# MAGIC #### Heatmap of Monthly Null Rates
# MAGIC ----
# MAGIC
# MAGIC - After January 2023 most of the data has a null rate of 0.8 or above. Given that most the of columns have such a high null rate at the start of that year, all rows with a date after December 2022 not be considered.

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

# MAGIC %md
# MAGIC #### Null Rates by Country

# COMMAND ----------

null_rates_by_country_df = spark.sql('''
-- Null rates over time by country 
with 
    covid_core_nulls 
as
(
    select
        country,
        case when code is null then 1 else 0 end as code_null,
        case when continent is null then 1 else 0 end as continent_null,
        case when population is null then 1 else 0 end as population_null,
        case when total_cases is null then 1 else 0 end as total_cases_null,
        case when new_cases is null then 1 else 0 end as new_cases_null,
        case when total_deaths is null then 1 else 0 end as total_deaths_null,
        case when new_deaths is null then 1 else 0 end as new_deaths_null,
        case when total_tests is null then 1 else 0 end as total_tests_null,
        case when new_tests is null then 1 else 0 end as new_tests_null,
        case when positive_rate is null then 1 else 0 end as positive_rate_null,
        case when tests_per_case is null then 1 else 0 end as tests_per_case_null,
        case when total_vaccinations is null then 1 else 0 end as total_vaccinations_null,
        case when people_vaccinated is null then 1 else 0 end as people_vaccinated_null,
        case when people_fully_vaccinated is null then 1 else 0 end as people_fully_vaccinated_null,
        case when total_boosters is null then 1 else 0 end as total_boosters_null,
        case when new_vaccinations is null then 1 else 0 end as new_vaccinations_null,
        case when hosp_patients is null then 1 else 0 end as hosp_patients_null,
        case when weekly_hosp_admissions is null then 1 else 0 end as weekly_hosp_admissions_null,
        case when icu_patients is null then 1 else 0 end as icu_patients_null,
        case when weekly_icu_admissions is null then 1 else 0 end as weekly_icu_admissions_null,
        case when excess_mortality is null then 1 else 0 end as excess_mortality_null,
        case when excess_mortality_cumulative is null then 1 else 0 end as excess_mortality_cumulative_null,
        case when excess_mortality_cumulative_absolute is null then 1 else 0 end as excess_mortality_cumulative_absolute_null,
        case when stringency_index is null then 1 else 0 end as stringency_index_null,
        case when reproduction_rate is null then 1 else 0 end as reproduction_rate_null
    from 
        covid_core_metrics
    where
        country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China, South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
)
select
    country,
    avg(code_null) as code_null_rate,
    avg(continent_null) as continent_null_rate,
    avg(population_null) as population_null_rate,
    avg(total_cases_null) as total_cases_null_rate,
    avg(new_cases_null) as new_cases_null_rate,
    avg(total_deaths_null) as total_deaths_null_rate,
    avg(new_deaths_null) as new_deaths_null_rate,
    avg(total_tests_null) as total_tests_null_rate,
    avg(new_tests_null) as new_tests_null_rate,
    avg(positive_rate_null) as positive_rate_null_rate,
    avg(tests_per_case_null) as tests_per_case_null_rate,
    avg(total_vaccinations_null) as total_vaccinations_null_rate,
    avg(people_vaccinated_null) as people_vaccinated_null_rate,
    avg(people_fully_vaccinated_null) as people_fully_vaccinated_null_rate,
    avg(total_boosters_null) as total_boosters_null_rate,
    avg(new_vaccinations_null) as new_vaccinations_null_rate,
    avg(hosp_patients_null) as hosp_patients_null_rate,
    avg(weekly_hosp_admissions_null) as weekly_hosp_admissions_null_rate,
    avg(icu_patients_null) as icu_patients_null_rate,
    avg(weekly_icu_admissions_null) as weekly_icu_admissions_null_rate,
    avg(excess_mortality_null) as excess_mortality_null_rate,
    avg(excess_mortality_cumulative_null) as excess_mortality_cumulative_null_rate,
    avg(excess_mortality_cumulative_absolute_null) as excess_mortality_cumulative_absolute_null_rate,
    avg(stringency_index_null) as stringency_index_null_rate,
    avg(reproduction_rate_null) as reproduction_rate_null_rate
from 
    covid_core_nulls
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
# MAGIC - The majority of countries are missing values in the same columns. So, dropping rows is not an option because it will significantly reduce the number of countries in the dataset.

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
# MAGIC ---
# MAGIC
# MAGIC - For simplicity's sake, we will remove records with null reproduction_rate and stringency_index for now. In the future, we will include these records and impute missing data.

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC   country,
# MAGIC   date,
# MAGIC   code,
# MAGIC   continent,
# MAGIC   total_cases,
# MAGIC   new_cases,
# MAGIC   total_deaths,
# MAGIC   new_deaths,
# MAGIC   stringency_index,
# MAGIC   reproduction_rate
# MAGIC from
# MAGIC     covid_owid_raw
# MAGIC where
# MAGIC     date < '2023-01-01'
# MAGIC     and country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China, South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
# MAGIC     and country is not null
# MAGIC     and date is not null
# MAGIC     and code is not null
# MAGIC     and continent is not null
# MAGIC     and total_cases is not null
# MAGIC     and new_cases is not null
# MAGIC     and total_deaths is not null
# MAGIC     and new_deaths is not null
# MAGIC     and stringency_index is not null
# MAGIC     and reproduction_rate is not null
# MAGIC order by
# MAGIC     country
# MAGIC ;

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