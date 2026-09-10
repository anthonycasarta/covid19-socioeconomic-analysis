create or refresh streaming table
    gold.covid_gdp_daily
as
select
    covid.code as country_code,
    covid.country,
    covid.continent,
    covid.date as observation_date,
    classification.gdp_per_capita,
    classification.gdp_cluster,
    covid.population,
    covid.new_cases,
    covid.new_deaths,
    covid.total_cases,
    covid.total_deaths,
    covid_normal.total_cases_per_million,
    covid_normal.total_deaths_per_million,
    classification.country is not null as is_gdp_classified
from stream
    silver.covid_core_metrics_daily as covid
left join
    silver.covid_normalized_metrics_daily as covid_normal
on
   covid.country = covid_normal.country
    and covid.date = covid_normal.date
left join
    gold.owid_gdp_classification as classification
on
    covid.country = classification.country
;
