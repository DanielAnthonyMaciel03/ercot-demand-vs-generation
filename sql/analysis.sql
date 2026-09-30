
-- Created a saved view isolating just the February 2021 winter storm period
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



-- Created a saved view summarizing average and worst cushion by month across all five years
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



-- Created a saved view showing average and worst cushion grouped by temperature bucket
CREATE VIEW view_cushion_by_temp_bucket AS
SELECT
  FLOOR(temperature / 5) * 5 AS temp_bucket,
  AVG(cushion) AS avg_cushion,
  MIN(cushion) AS worst_cushion,
  COUNT(*) AS num_hours
FROM ercot_hourly_data
GROUP BY temp_bucket
ORDER BY temp_bucket;