
-- Isolates the February 2021 winter storm period for close inspection of the grid's worst crisis event
CREATE VIEW view_feb2021_freeze AS
SELECT
  period,
  demand,
  net_generation,
  cushion,
  temperature
FROM ercot_hourly_data
WHERE period BETWEEN '2021-02-10' AND '2021-02-20'
ORDER BY period;


-- Summarizes average temperature, average cushion, and worst cushion by month across all five years
CREATE VIEW view_monthly_summary AS
SELECT
  DATE_TRUNC('month', period) AS month,
  EXTRACT(YEAR FROM period) AS year,
  AVG(temperature) AS avg_temp,
  AVG(cushion) AS avg_cushion,
  MIN(cushion) AS worst_cushion
FROM ercot_hourly_data
GROUP BY month, year
ORDER BY month;


-- Groups every hour into 5-degree temperature ranges to reveal the relationship between temperature and cushion
CREATE VIEW view_cushion_by_temp_bucket AS
SELECT
  FLOOR(temperature / 5) * 5 AS temp_bucket,
  AVG(cushion) AS avg_cushion,
  MIN(cushion) AS worst_cushion,
  COUNT(*) AS num_hours
FROM ercot_hourly_data
GROUP BY temp_bucket
ORDER BY temp_bucket;


-- Adds year, month, day, and hour breakdowns to the hourly data, used to power the hour-of-day chart and its drill-down by month
CREATE VIEW view_hourly_with_month AS
SELECT
  period,
  DATE_TRUNC('month', period) AS month,
  EXTRACT(YEAR FROM period) AS year,
  EXTRACT(DAY FROM period) AS day_of_month,
  EXTRACT(HOUR FROM period) AS hour_of_day,
  demand,
  net_generation,
  cushion,
  temperature
FROM ercot_hourly_data;