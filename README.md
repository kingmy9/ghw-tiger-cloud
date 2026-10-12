# GHW Hacktoberfest – Tiger Cloud challenges

Work done on a free Tiger Cloud service (`db-83026`, AWS us-east-1, PostgreSQL 18.6, TimescaleDB 2.30.2) for MLH Global Hack Week.

| Challenge | File | Result |
|---|---|---|
| Set up a Tiger Cloud service and create your first Hypertable | `01_hypertable_iot.sql` | `sensor_data` created as a hypertable (`create_hypertable('sensor_data', by_range('time'))`), shown under Hypertables in the console Explorer |
| Simulate an IoT sensor dataset | `01_hypertable_iot.sql` | 4 sensors, 24 h of 5‑minute readings (1,156 rows); 30‑minute `time_bucket` averages query returns 10 rows |
| Accelerate Dashboards with Continuous Aggregates | `02_continuous_aggregate.sql` | `sensor_hourly` continuous aggregate (hourly avg/min/max per sensor) + refresh policy (background job 1001) |
| AI-Powered Vector Search with pgvector | `03_vector_search.sql` | `event_embeddings` with `vector(3)`; cosine similarity search filtered to the last 24 h |

## Vector search output

| label | cosine_distance |
|---|---|
| overheat alert | 0.0061 |
| fan failure | 0.0369 |
| normal reading | 0.8902 |

The 30‑hour‑old "old overheat" row is correctly excluded by the time filter.

## Run it yourself

Create a free service at https://console.cloud.tigerdata.com, open the SQL editor and run the files in order.
