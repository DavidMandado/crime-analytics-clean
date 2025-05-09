CREATE TABLE processed_data AS
SELECT 
    CrimeID,
    Month,
	year,
    Reportedby,
    Fallswithin,
    Longitude,
    Latitude,
    Location,
    LSOAcode,
    LSOAname,
    Outcometype,
    Crimetype,
    Lastoutcomecategory
FROM raw_data;