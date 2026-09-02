create or refresh streaming table
    silver.covid_core_metrics_daily
as
select
    country,
    date,
    code,
    continent,
    total_cases,
    new_cases,
    total_deaths,
    new_deaths,
    stringency_index,
    reproduction_rate
from stream 
    covid_owid_raw
where
    date < '2023-01-01'
    and country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China, South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
    and country is not null
    and date is not null
    and code is not null
    and continent is not null
    and total_cases is not null
    and new_cases is not null
    and total_deaths is not null
    and new_deaths is not null
    and stringency_index is not null
    and reproduction_rate is not null
;
