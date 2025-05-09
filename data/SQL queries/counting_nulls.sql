-- This serves to calculate the amount of null values in each attribute, i have to do one by one since all at once crashed the app.
SELECT
  COUNT(*)                AS total_rows,
  COUNT("LSOAcode")         AS non_null,
  COUNT(*) - COUNT("LSOAcode") AS null_count,
  ROUND((COUNT(*)-COUNT("LSOAcode"))*100.0/COUNT(*),2) AS null_pct,
  COUNT(DISTINCT "LSOAcode") AS distinct_vals
FROM vw_residential_burglary;
