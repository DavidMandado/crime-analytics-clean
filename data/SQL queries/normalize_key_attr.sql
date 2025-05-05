UPDATE burglary_cleaned
SET
  Crimetype           = LOWER(TRIM(Crimetype)),
  Lastoutcomecategory = LOWER(TRIM(Lastoutcomecategory)),
  Location            = TRIM(Location);
