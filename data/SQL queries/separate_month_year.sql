UPDATE burglary_data
SET
  year  = CAST(SUBSTR(Month,1,4) AS INTEGER),
  month = CAST(SUBSTR(Month,6,2) AS INTEGER);
