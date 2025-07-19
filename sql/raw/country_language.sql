CREATE TABLE IF NOT EXISTS raw.country_language (
    id SERIAL PRIMARY KEY,
    country_name VARCHAR(255) NOT NULL,
    language_code VARCHAR(3) NOT NULL
);

COPY raw.country_language (id, country_name, language_code)
FROM '<csv_file_path>'
WITH (FORMAT csv, HEADER);