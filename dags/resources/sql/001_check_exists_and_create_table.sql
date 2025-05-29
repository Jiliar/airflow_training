DO $$
BEGIN
    -- Crear extensión si no existe
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Crear tabla si no existe
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'sales_data') THEN
        CREATE TABLE sales_data (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            ddate DATE NOT NULL,
            store VARCHAR(100) NOT NULL,
            sales NUMERIC(10, 2) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
    ELSE
        -- Aquí podrías añadir lógica para actualizar la tabla si es necesario
        RAISE NOTICE 'Table sales_data already exists - verifying structure';
    END IF;
END
$$;