CREATE TABLE IF NOT EXISTS country_language (
    id SERIAL PRIMARY KEY,
    country_name VARCHAR(3) NOT NULL,
    currency_code VARCHAR(3) NOT NULL
);