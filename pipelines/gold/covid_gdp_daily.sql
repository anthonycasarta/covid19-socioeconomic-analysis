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
    covid.stringency_index,
    covid.reproduction_rate,
    classification.country is not null as is_gdp_classified
from stream
    silver.covid_core_metrics_daily as covid
left join
    gold.owid_gdp_classification as classification
on
    covid.country = classification.country
;
