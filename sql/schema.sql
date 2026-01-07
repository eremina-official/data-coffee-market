-- ========================================
-- Schema for Polish Independent Coffee Market
-- ========================================

-- Create new database (ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci)
-- Create tables

-- ========================================
-- Table: sellers
-- Stores seller info and ratings
-- ========================================
CREATE TABLE IF NOT EXISTS sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_name VARCHAR(255),
    avg_rating DECIMAL(3,2),
    ratings_count INT,
    recommended_pct INT
);

-- ========================================
-- Table: offers
-- Stores static info about coffee offers
-- ========================================
CREATE TABLE IF NOT EXISTS offers (
    offer_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255),
    brand VARCHAR(100),
    origin_country VARCHAR(100),
    weight_g INT,
    roast_level VARCHAR(50),
    is_specialty BOOLEAN,
    roaster_type VARCHAR(20),
    seller_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ========================================
-- Table: offer_prices
-- Stores time-series snapshots of offer prices
-- ========================================
CREATE TABLE IF NOT EXISTS offer_prices (
    offer_id VARCHAR(50),
    snapshot_date DATE,
    price DECIMAL(10,2),
    currency CHAR(3) DEFAULT 'PLN',
    PRIMARY KEY (offer_id, snapshot_date),
    FOREIGN KEY (offer_id) REFERENCES offers(offer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ========================================
-- Indexes for faster analytics
-- ========================================
CREATE INDEX idx_offer_origin ON offers(origin_country);
CREATE INDEX idx_offer_brand ON offers(brand);
CREATE INDEX idx_price_snapshot ON offer_prices(snapshot_date);

-- ========================================
-- End of schema
-- ========================================
