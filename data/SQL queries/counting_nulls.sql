-- This serves to calculate the amount of null values in each attribute, i have to do one by one since all at once crashed the app.
SELECT
  COUNT(*)                AS total_rows,
  COUNT("COLUMN")         AS non_null,
  COUNT(*) - COUNT("COLUMN") AS null_count,
  ROUND((COUNT(*)-COUNT("COLUMN"))*100.0/COUNT(*),2) AS null_pct,
  COUNT(DISTINCT "COLUMN") AS distinct_vals
FROM burglary_data;
