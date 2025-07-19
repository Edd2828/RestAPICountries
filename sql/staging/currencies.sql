CREATE TABLE IF NOT EXISTS staging.currencies (
    id SERIAL PRIMARY KEY,
    code VARCHAR(3) NOT NULL,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10)
);

COPY staging.currencies (id, code, name, symbol)
FROM '<csv_file_path>'
WITH (FORMAT csv, HEADER);