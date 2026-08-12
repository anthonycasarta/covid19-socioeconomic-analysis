CREATE OR REFRESH STREAMING TABLE
covid19_socioeconomic_analysis.bronze.covid_owid_raw
AS SELECT *
FROM STREAM read_files(
"/Volumes/covid19_socioeconomic_analysis/bronze/covid_raw/owid/data/",
format => "csv",
header => true,
)

