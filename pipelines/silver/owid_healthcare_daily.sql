create or refresh streaming table
    silver.owid_healthcare_daily
as
select
    country,
    date,
    population_density,
    median_age,
    life_expectancy,
    diabetes_prevalence,
    hospital_beds_per_thousand
from 
    bronze.covid_owid_raw
where
    country not in ('Asia excl. China',  'World', 'World excl. China', 'World excl. China and South Korea', 'World excl. China, South Korea, Japan and Singapore', 'Winter Olympics 2022', 'Summer Olympics 2020', 'Low-income countries', 'Lower-middle-income countries', 'High-income countries', 'European Union (27)')
    and country is not null
    and date is not null
    and population_density is not null
    and median_age is not null
    and life_expectancy is not null
    and diabetes_prevalence is not null
    and hospital_beds_per_thousand is not null
;
