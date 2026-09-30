
-- 1) Create the schema in order to load in our data into postgreSQL
CREATE TABLE ercot_hourly_data (
    period timestamp PRIMARY KEY,
    demand numeric,
    day_ahead_forecast numeric,
    net_generation numeric,
    total_interchange numeric,
    hour timestamp,
    temperature numeric
);


-- 2) the 'hour' column is a duplicate of the 'period' column, so I chose to set 'period as the PRIMARY KEY and drop 'hour'
ALTER TABLE ercot_hourly_data DROP COLUMN hour;



-- 3) In this project specifically I decided to perform data cleaning with SQL, So the following queries
-- helped me determine if there were any impossible values, outliers, or null values in the dataset


-- Check for impossible values for 'demand' and 'net_generation'
SELECT * FROM ercot_hourly_data WHERE demand < 0;
SELECT * FROM ercot_hourly_data WHERE net_generation < 0;

-- Check for outlier 'temperature' values, Houston shouldnt be negative or exceed around 115 fahrenheit 
SELECT * FROM ercot_hourly_data WHERE temperature < 0 OR temperature > 115;

-- Check for duplicate time stamps
SELECT period, COUNT(*)
FROM ercot_hourly_data
GROUP BY period
HAVING COUNT(*) > 1;

-- Check for NULL values across all columns
SELECT
  COUNT(*) FILTER (WHERE demand IS NULL) AS null_demand,
  COUNT(*) FILTER (WHERE net_generation IS NULL) AS null_generation,
  COUNT(*) FILTER (WHERE temperature IS NULL) AS null_temp,
  COUNT(*) FILTER (WHERE total_interchange IS NULL) AS null_interchange
FROM ercot_hourly_data;

    -- 9 NULL values returned specifically from 'total_interchange', handled by removing those rows
        DELETE FROM ercot_hourly_data 
        WHERE total_interchange IS NULL;


-- 4) Introduce the 'cushion' column and calculate the values
ALTER TABLE ercot_hourly_data ADD COLUMN cushion numeric;

UPDATE ercot_hourly_data
SET cushion = net_generation - demand;