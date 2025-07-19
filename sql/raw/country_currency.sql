CREATE TABLE IF NOT EXISTS raw.country_currency (
    id SERIAL PRIMARY KEY,
    country_name VARCHAR(255) NOT NULL,
    currency_code VARCHAR(3) NOT NULL
);

COPY raw.country_currency (id, country_name, currency_code)
FROM '<csv_file_path>'
WITH (FORMAT csv, HEADER);