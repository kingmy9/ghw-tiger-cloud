# Tiger CLI + Tiger MCP with an AI agent

The AI agent here is **Hark** (an AI assistant), connected to Tiger Cloud through the Tiger MCP server bundled in Tiger CLI.

## Setup
```bash
curl -fsSL https://cli.tigerdata.com | sh     # Tiger CLI 0.26.0
tiger auth login --headless                    # device-code OAuth, authorized in the Tiger console
tiger mcp start                                # stdio MCP server the agent talks to
```
`mcp_client.py` is the small JSON-RPC (stdio) bridge the agent used to call MCP tools.

## Tools exposed by Tiger MCP
db_query, db_schema, search_docs, service_create, service_delete, service_fork, service_get, service_list, service_logs, service_metrics_*, service_rename, service_resize, service_start, service_stop, service_update_password, view_skill, feedback

## Agent session
**Ask:** "Which Tiger Cloud services do I have?" → tool `service_list`
```
db-83026 (ukv0jjtgqx) · TIMESCALEDB · READY · us-east-1 · shared CPU/memory · DEV
```

**Ask:** "What's the average temperature per sensor in my IoT data?" → tool `db_query`
```sql
SELECT sensor_id, round(avg(temperature)::numeric,2) AS avg_temp, count(*) AS readings
FROM sensor_data GROUP BY sensor_id ORDER BY sensor_id;
```
| sensor_id | avg_temp | readings |
|---|---|---|
| 1 | 50.62 | 289 |
| 2 | 50.93 | 289 |
| 3 | 51.18 | 289 |
| 4 | 50.41 | 289 |
(66 ms)
