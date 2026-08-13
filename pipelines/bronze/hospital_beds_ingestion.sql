CREATE OR REFRESH STREAMING TABLE
 bronze.hospital_beds_raw
 TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
 AS SELECT *
 FROM STREAM read_files(
     "${hospital_beds_source}",
     format => 'csv',
     header => true
     );

