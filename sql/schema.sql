-- ==================================================
-- Coffee Market Database Schema
-- ==================================================

-- 1. Products table
CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    publication_status VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Categories table
CREATE TABLE IF NOT EXISTS categories (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id VARCHAR(50),
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

-- 3. Product-Categories mapping
CREATE TABLE IF NOT EXISTS product_categories (
    product_id VARCHAR(50),
    category_id VARCHAR(50),
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- 4. Parameters table
CREATE TABLE IF NOT EXISTS parameters (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50),
    identifies_product BOOLEAN DEFAULT FALSE
);

-- 5. Parameter Values table
CREATE TABLE IF NOT EXISTS parameter_values (
    id VARCHAR(50) PRIMARY KEY,
    parameter_id VARCHAR(50),
    label VARCHAR(255),
    value VARCHAR(255),
    FOREIGN KEY (parameter_id) REFERENCES parameters(id)
);

-- 6. Product-ParameterValues mapping
CREATE TABLE IF NOT EXISTS product_parameter_values (
    product_id VARCHAR(50),
    value_id VARCHAR(50),
    PRIMARY KEY (product_id, value_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (value_id) REFERENCES parameter_values(id)
);

-- 7. Images table
CREATE TABLE IF NOT EXISTS images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url TEXT NOT NULL
);

-- 8. Product-Images mapping
CREATE TABLE IF NOT EXISTS product_images (
    product_id VARCHAR(50),
    image_id INT,
    PRIMARY KEY (product_id, image_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (image_id) REFERENCES images(id)
);

-- 9. Optional: Responsible Producers (from productSafety)
CREATE TABLE IF NOT EXISTS producers (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    trade_name VARCHAR(255),
    street VARCHAR(255),
    postal_code VARCHAR(20),
    city VARCHAR(100),
    country_code VARCHAR(10),
    email VARCHAR(255),
    phone_number VARCHAR(50),
    form_url VARCHAR(255)
);

-- 10. Product-Producers mapping
CREATE TABLE IF NOT EXISTS product_producers (
    product_id VARCHAR(50),
    producer_id VARCHAR(50),
    PRIMARY KEY (product_id, producer_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (producer_id) REFERENCES producers(id)
);
