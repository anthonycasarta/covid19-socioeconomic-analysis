CREATE OR REPLACE VIEW covid19_socioeconomic_analysis.gold.covid_gdp_metric_view
WITH METRICS LANGUAGE YAML AS $$
version: 1.1
source: covid19_socioeconomic_analysis.gold.covid_gdp_daily

fields:
  - name: date
    expr: observation_date
  - name: week
    expr: DATE_TRUNC('WEEK', date)
  - name: month
    expr: DATE_TRUNC('MONTH', date)
  - name: year
    expr: DATE_TRUNC('YEAR', date)
  - name: country
    expr: country
  - name: continent
    expr: continent
  - name: gdp_cluster
    expr: gdp_cluster

measures:
  - name: reported_cases
    expr: SUM(new_cases)
  - name: reported_deaths
    expr: SUM(new_deaths)
  - name: population
    expr: SUM(population)
    window:
      - order: date
        range: current
        semiadditive: last
  - name: cases_per_million
    expr: SUM(total_cases_per_million)
    window:
      - order: date
        semiadditive: last
        range: current
$$;
