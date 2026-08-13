 CREATE OR REFRESH STREAMING TABLE
bronze.hospital_density_raw
 TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
 AS SELECT *
 FROM STREAM read_files(
     "${hospital_density_source}",
     format => 'csv',
     header => true
     );

