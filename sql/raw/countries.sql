CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    common_name VARCHAR(255) NOT NULL,
    official_name VARCHAR(255) NOT NULL,
    population BIGINT NOT NULL
);