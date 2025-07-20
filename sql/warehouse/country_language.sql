DO $$
BEGIN

    CREATE TABLE IF NOT EXISTS warehouse.country_language (
        id SERIAL PRIMARY KEY,
        country_name VARCHAR(255) NOT NULL,
        language_code VARCHAR(3) NOT NULL
    );


    INSERT INTO warehouse.country_language (id, country_name, language_code)
    SELECT id, country_name, language_code
    FROM staging.country_language
    ON CONFLICT (id) DO UPDATE
    SET country_name = EXCLUDED.country_name,
        language_code = EXCLUDED.language_code;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        
END $$;