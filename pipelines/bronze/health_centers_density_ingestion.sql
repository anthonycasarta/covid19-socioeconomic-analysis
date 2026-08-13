CREATE OR REFRESH STREAMING TABLE
bronze.health_centers_density_raw
TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
AS SELECT *
FROM STREAM read_files(
     "${health_centers_density_source}",
     format => "csv",
     header => true
     );

