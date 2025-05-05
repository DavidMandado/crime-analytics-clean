-- a) composite index on year & month for fast time‐series grouping
CREATE INDEX IF NOT EXISTS idx_bd_year_month
  ON burglary_data(year, month);

-- b) index on LSOAcode for quick spatial joins / aggregations
CREATE INDEX IF NOT EXISTS idx_bd_lsoa
  ON burglary_data(LSOAcode);

-- c) index on Crimetype to accelerate filtering by crime type
CREATE INDEX IF NOT EXISTS idx_bd_crimetype
  ON burglary_data(Crimetype);

-- d) optional: index on Longitude/Latitude if you do range or bounding‐box lookups
CREATE INDEX IF NOT EXISTS idx_bd_lonlat
  ON burglary_data(Longitude, Latitude);
