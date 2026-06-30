--products instance
CREATE TABLE IF NOT EXISTS products(
    product_id      BIGSERIAL PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    url             TEXT NOT NULL UNIQUE,
    marketplace     VARCHAR(255) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT ck_marketplace CHECK (marketplace IN ('MercadoLibre','Amazon', 'Walmart', 'Liverpool'))
);


--prices instance
CREATE TABLE IF NOT EXISTS prices(
    price_id        BIGSERIAL PRIMARY KEY,
    price           NUMERIC(10, 2) NOT NULL,
    has_stock       BOOLEAN NOT NULL DEFAULT TRUE,
    scraped_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Foreign key 
    product_id         BIGINT NOT NULL REFERENCES products(product_id) ON DELETE CASCADE
);

