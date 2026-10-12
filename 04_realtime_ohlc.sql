-- 1-minute OHLC candles from live ticks (time_bucket + first/last)
SELECT time_bucket('1 minute', time) AS minute, symbol,
       first(price, time) AS open, max(price) AS high, min(price) AS low, last(price, time) AS close,
       count(*) AS ticks
FROM crypto_ticks GROUP BY minute, symbol ORDER BY minute DESC, symbol LIMIT 15;

-- Latest price, spread and 10-min move per symbol
SELECT symbol, last(price, time) AS last_price,
       round((last(best_ask,time)-last(best_bid,time))::numeric, 4) AS spread,
       round(((last(price,time)/first(price,time)-1)*100)::numeric, 3) AS pct_change,
       count(*) AS ticks
FROM crypto_ticks GROUP BY symbol ORDER BY symbol;
