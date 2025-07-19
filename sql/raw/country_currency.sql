CREATE TABLE IF NOT EXISTS country_currency (
    id SERIAL PRIMARY KEY,
    country_name VARCHAR(255) NOT NULL,
    currency_code VARCHAR(3) NOT NULL
);