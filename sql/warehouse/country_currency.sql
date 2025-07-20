DO $$
BEGIN

    CREATE TABLE IF NOT EXISTS warehouse.country_currency (
        id SERIAL PRIMARY KEY,
        country_name VARCHAR(255) NOT NULL,
        currency_code VARCHAR(3) NOT NULL
    );


    INSERT INTO warehouse.country_currency (id, country_name, currency_code)
    SELECT id, country_name, currency_code
    FROM staging.country_currency
    ON CONFLICT (id) DO UPDATE
    SET country_name = EXCLUDED.country_name,
        currency_code = EXCLUDED.currency_code;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        
END $$;