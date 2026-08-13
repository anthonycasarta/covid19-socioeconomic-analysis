
CREATE OR REFRESH STREAMING TABLE
    silver.covid_daily
COMMENT 'Cleaned daily country-level COVID-19 time-series data'
AS
SELECT
    UPPER(TRIM(code)) AS country_code,
    TRIM(country) AS country_name,
    TRIM(continent) AS continent,
    TRY_CAST(`date` AS DATE) AS observation_date,

    -- Country attributes
    TRY_CAST(population AS BIGINT) AS population,
    TRY_CAST(population_density AS DOUBLE) AS population_density,
    TRY_CAST(median_age AS DOUBLE) AS median_age,
    TRY_CAST(life_expectancy AS DOUBLE) AS life_expectancy,
    TRY_CAST(gdp_per_capita AS DOUBLE) AS gdp_per_capita,
    TRY_CAST(extreme_poverty AS DOUBLE) AS extreme_poverty,
    TRY_CAST(diabetes_prevalence AS DOUBLE) AS diabetes_prevalence,
    TRY_CAST(hospital_beds_per_thousand AS DOUBLE)
        AS hospital_beds_per_thousand,

    -- Daily cases
    TRY_CAST(new_cases AS DOUBLE) AS new_cases,
    TRY_CAST(new_cases_per_million AS DOUBLE)
        AS new_cases_per_million,
    TRY_CAST(new_cases_smoothed AS DOUBLE)
        AS new_cases_smoothed,
    TRY_CAST(new_cases_smoothed_per_million AS DOUBLE)
        AS new_cases_smoothed_per_million,

    -- Cumulative cases
    TRY_CAST(total_cases AS DOUBLE) AS total_cases,
    TRY_CAST(total_cases_per_million AS DOUBLE)
        AS total_cases_per_million,

    -- Daily deaths
    TRY_CAST(new_deaths AS DOUBLE) AS new_deaths,
    TRY_CAST(new_deaths_per_million AS DOUBLE)
        AS new_deaths_per_million,
    TRY_CAST(new_deaths_smoothed AS DOUBLE)
        AS new_deaths_smoothed,
    TRY_CAST(new_deaths_smoothed_per_million AS DOUBLE)
        AS new_deaths_smoothed_per_million,

    -- Cumulative deaths
    TRY_CAST(total_deaths AS DOUBLE) AS total_deaths,
    TRY_CAST(total_deaths_per_million AS DOUBLE)
        AS total_deaths_per_million,
    COALESCE(new_cases < 0, FALSE)
        AS has_negative_case_correction,
    COALESCE(new_deaths < 0, FALSE)
        AS has_negative_death_correction

FROM STREAM
    bronze.covid_owid_raw;
-- WHERE country_code RLIKE '^[A-Z]{3}$'
--     AND observation_date IS NOT NULL;
    
    
