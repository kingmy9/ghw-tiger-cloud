"""Real-time crypto price pipeline: Coinbase Exchange public WebSocket -> Tiger Cloud hypertable."""
import asyncio, json, os, sys, time
import psycopg2, websockets
from psycopg2.extras import execute_values

DSN = dict(host="ukv0jjtgqx.p08q2ys4sc.tsdb.cloud.timescale.com", port=39028, dbname="tsdb",
           user="tsdbadmin", sslmode="require")  # password from PGPASSFILE / PGPASSWORD
PRODUCTS = ["BTC-USD", "ETH-USD", "SOL-USD"]
RUN_SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 300

SCHEMA = """
CREATE TABLE IF NOT EXISTS crypto_ticks (
  time TIMESTAMPTZ NOT NULL, symbol TEXT NOT NULL, price DOUBLE PRECISION,
  best_bid DOUBLE PRECISION, best_ask DOUBLE PRECISION, last_size DOUBLE PRECISION, volume_24h DOUBLE PRECISION);
SELECT create_hypertable('crypto_ticks', by_range('time'), if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS crypto_ticks_symbol_time ON crypto_ticks (symbol, time DESC);
"""

async def main():
    conn = psycopg2.connect(**DSN); conn.autocommit = True
    cur = conn.cursor(); cur.execute(SCHEMA)
    buf, total, end = [], 0, time.time() + RUN_SECONDS
    async with websockets.connect("wss://ws-feed.exchange.coinbase.com") as ws:
        await ws.send(json.dumps({"type": "subscribe", "product_ids": PRODUCTS, "channels": ["ticker"]}))
        while time.time() < end:
            m = json.loads(await asyncio.wait_for(ws.recv(), 30))
            if m.get("type") != "ticker": continue
            buf.append((m["time"], m["product_id"], float(m["price"]), float(m["best_bid"]),
                        float(m["best_ask"]), float(m.get("last_size") or 0), float(m["volume_24h"])))
            if len(buf) >= 50:
                execute_values(cur, "INSERT INTO crypto_ticks VALUES %s", buf); total += len(buf); buf = []
                print(f"inserted {total} ticks", flush=True)
    if buf: execute_values(cur, "INSERT INTO crypto_ticks VALUES %s", buf); total += len(buf)
    print("done, total", total)

asyncio.run(main())
