DO $$
BEGIN

    CREATE TABLE IF NOT EXISTS warehouse.currencies (
        id SERIAL PRIMARY KEY,
        code VARCHAR(3) NOT NULL,
        name VARCHAR(100) NOT NULL,
        symbol VARCHAR(10)
    );


    INSERT INTO warehouse.currencies (id, code, name, symbol)
    SELECT id, code, name, symbol
    FROM staging.currencies
    ON CONFLICT (id) DO UPDATE
    SET code = EXCLUDED.code,
        name = EXCLUDED.name,
        symbol = EXCLUDED.symbol;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        
END $$;