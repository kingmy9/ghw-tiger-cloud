-- pgvector similarity search filtered by time
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE event_embeddings (time TIMESTAMPTZ NOT NULL, label TEXT, embedding vector(3));
INSERT INTO event_embeddings VALUES
 (now() - interval '1 hour', 'overheat alert', '[0.9,0.1,0.0]'),
 (now() - interval '2 hour', 'normal reading', '[0.1,0.9,0.1]'),
 (now() - interval '3 hour', 'fan failure', '[0.8,0.2,0.1]'),
 (now() - interval '30 hour', 'old overheat', '[0.95,0.05,0.0]');
SELECT label, time, embedding <=> '[1,0,0]' AS cosine_distance
FROM event_embeddings WHERE time > now() - interval '24 hours'
ORDER BY embedding <=> '[1,0,0]' LIMIT 3;
