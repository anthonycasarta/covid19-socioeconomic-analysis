CREATE OR REFRESH STREAMING TABLE
covid19_socioeconomic_analysis.bronze.health_centers_density_raw
TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
AS SELECT *
FROM STREAM read_files(
     "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/source_a/health_centers_density/data/",
     format => "csv",
     header => true
     );

