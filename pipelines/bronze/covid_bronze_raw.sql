CREATE OR REFRESH STREAMING TABLE
    bronze.covid_owid_raw
AS SELECT *
FROM STREAM read_files(
'${covid_source}',
format => "csv",
header => true
);

