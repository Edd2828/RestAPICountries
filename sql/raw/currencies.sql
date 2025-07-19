CREATE TABLE IF NOT EXISTS raw.currencies (
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) NOT NULL,
    symbol VARCHAR(10)
);

COPY raw.currencies (id, code, symbol)
FROM '<csv_file_path>'
WITH (FORMAT csv, HEADER);