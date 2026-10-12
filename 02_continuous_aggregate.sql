-- Continuous aggregate: hourly metrics per sensor
CREATE MATERIALIZED VIEW sensor_hourly WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) AS bucket, sensor_id,
       AVG(temperature) AS avg_temp, MIN(temperature) AS min_temp, MAX(temperature) AS max_temp
FROM sensor_data GROUP BY bucket, sensor_id;
SELECT add_continuous_aggregate_policy('sensor_hourly', start_offset => INTERVAL '3 days', end_offset => INTERVAL '1 hour', schedule_interval => INTERVAL '1 hour');
SELECT * FROM sensor_hourly ORDER BY bucket DESC, sensor_id LIMIT 10;
