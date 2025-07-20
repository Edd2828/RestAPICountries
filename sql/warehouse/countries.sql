DO $$
BEGIN

    CREATE TABLE IF NOT EXISTS warehouse.countries (
        id SERIAL PRIMARY KEY,
        common_name VARCHAR(255) NOT NULL,
        official_name VARCHAR(255) NOT NULL,
        population BIGINT NOT NULL
    );

    INSERT INTO warehouse.countries (id, common_name, official_name, population)
    SELECT id, common_name, official_name, population
    FROM staging.countries
    ON CONFLICT (id) DO UPDATE
    SET common_name = EXCLUDED.common_name,
        official_name = EXCLUDED.official_name,
        population = EXCLUDED.population;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        
END $$;