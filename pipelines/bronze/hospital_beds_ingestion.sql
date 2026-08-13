CREATE OR REFRESH STREAMING TABLE
 covid19_socioeconomic_analysis.bronze.hospital_beds_raw
 TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
 AS SELECT *
 FROM STREAM read_files(
     "/Volumes/covid19_socioeconomic_analysis/bronze/healthcare_raw/source_a/hospital_beds/data/",
     format => 'csv',
     header => true
     );

