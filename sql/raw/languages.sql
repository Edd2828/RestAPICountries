CREATE TABLE IF NOT EXISTS raw.languages (
    id INT PRIMARY KEY,
    code VARCHAR(3) NOT NULL,
    name VARCHAR(100) NOT NULL
);

COPY raw.languages (id, code, name)
FROM '<csv_file_path>'
WITH (FORMAT csv, HEADER);