-- Hypertable + simulated IoT sensor data
CREATE TABLE sensors (id SERIAL PRIMARY KEY, type VARCHAR(50), location VARCHAR(50));
CREATE TABLE sensor_data (time TIMESTAMPTZ NOT NULL, sensor_id INTEGER, temperature DOUBLE PRECISION, cpu DOUBLE PRECISION);
SELECT create_hypertable('sensor_data', by_range('time'));
INSERT INTO sensors (type, location) VALUES ('a','floor'),('a','ceiling'),('b','floor'),('b','ceiling');
INSERT INTO sensor_data (time, sensor_id, cpu, temperature)
SELECT time, sensor_id, random() AS cpu, random()*100 AS temperature
FROM generate_series(now() - interval '24 hour', now(), interval '5 minute') AS g1(time),
     generate_series(1,4,1) AS g2(sensor_id);
SELECT time_bucket('30 minutes', time) AS period, AVG(temperature) AS avg_temp, AVG(cpu) AS avg_cpu
FROM sensor_data GROUP BY period ORDER BY period DESC LIMIT 10;
