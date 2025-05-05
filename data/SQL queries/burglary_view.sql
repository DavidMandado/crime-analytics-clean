DROP VIEW IF EXISTS vw_residential_burglary;
CREATE VIEW vw_residential_burglary AS
SELECT *
FROM burglary_data
WHERE Crimetype = 'burglary';