CREATE TABLE IF NOT EXISTS staging.languages (
    id INT PRIMARY KEY,
    code VARCHAR(3) NOT NULL,
    name VARCHAR(100) NOT NULL
);

COPY staging.languages (id, code, name)
FROM '<csv_file_path>'
WITH (FORMAT csv, HEADER);