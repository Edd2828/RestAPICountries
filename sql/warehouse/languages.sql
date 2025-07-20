DO $$
BEGIN

    CREATE TABLE IF NOT EXISTS warehouse.languages (
        id SERIAL PRIMARY KEY,
        code VARCHAR(3) NOT NULL,
        name VARCHAR(100) NOT NULL
    );

    INSERT INTO warehouse.languages (id, code, name)
    SELECT id, code, name
    FROM staging.languages
    ON CONFLICT (id) DO UPDATE
    SET code = EXCLUDED.code,
        name = EXCLUDED.name;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        
END $$;