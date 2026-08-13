 CREATE OR REFRESH STREAMING TABLE
 bronze.hospital_medicine_raw
 TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
 AS SELECT *
 FROM STREAM read_files(
     "${hospital_medicine_source}",
     format => 'csv',
     header => true
     );

