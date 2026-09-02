create or refresh streaming table
    silver.covid_normalized_metrics_daily
as
select
    country,
    date,
    new_cases_per_million,
    new_cases_smoothed,
    total_cases_per_million,
    new_deaths_per_million,
    new_deaths_smoothed,
    new_deaths_smoothed_per_million,
    total_deaths_per_million
from stream
    bronze.covid_owid_raw
where
    date < '2023-01-01'
    and country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China, South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
    and country is not null
    and new_cases_per_million is not null
    and new_cases_smoothed is not null
    and total_cases_per_million is not null
    and new_deaths_per_million is not null
    and new_deaths_smoothed is not null
    and new_deaths_smoothed_per_million is not null
    and total_deaths_per_million is not null
;
