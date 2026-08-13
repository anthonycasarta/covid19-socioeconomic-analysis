 CREATE OR REFRESH STREAMING TABLE
 covid19_socioeconomic_analysis.bronze.hospital_medicine_raw
 TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
 AS SELECT *
 FROM STREAM read_files(
     "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/source_a/hospital_medicine/data/",
     format => 'csv',
     header => true
     );

