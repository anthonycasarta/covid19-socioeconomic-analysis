 CREATE OR REFRESH STREAMING TABLE
 bronze.gdp_world_bank_raw
 TBLPROPERTIES ('delta.columnMapping.mode' = 'name')
 AS SELECT *
 FROM STREAM read_files("${gdp_source}");

