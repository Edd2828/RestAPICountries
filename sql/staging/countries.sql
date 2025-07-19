CREATE TABLE IF NOT EXISTS staging.countries (
    id SERIAL PRIMARY KEY,
    common_name VARCHAR(255) NOT NULL,
    official_name VARCHAR(255) NOT NULL,
    population BIGINT NOT NULL
);

COPY staging.countries (id, common_name, official_name, population)
FROM '<csv_file_path>'
WITH (FORMAT csv, HEADER);