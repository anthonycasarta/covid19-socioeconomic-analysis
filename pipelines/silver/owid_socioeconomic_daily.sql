create or refresh streaming table
    silver.owid_socioeconomic_daily
as
select
    country,
    date,
    gdp_per_capita,
    extreme_poverty
from stream
    bronze.owid_covid_raw
where
    date < '2023-01-01'
    and country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China and South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
    and country is not null
    and gdp_per_capita is not null
    and extreme_poverty is not null
;
