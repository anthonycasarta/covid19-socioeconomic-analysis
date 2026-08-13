 CREATE OR REFRESH STREAMING TABLE
 covid19_socioeconomic_analysis.bronze.gdp_world_bank_raw
 TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
 AS SELECT *
 FROM STREAM read_files("/Volumes/covid19_socioeconomic_analysis/bronze/gdp_raw/world_bank/data/");

