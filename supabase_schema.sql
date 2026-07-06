-- Dark Fashions Supabase Schema
-- Run this in Supabase SQL Editor (https://supabase.com/dashboard/project/buwkgovwcbrumamysbvu/sql/new)

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    image_url VARCHAR(500),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cart (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INT NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    shipping_address TEXT,
    pincode VARCHAR(10),
    payment_method VARCHAR(50) DEFAULT 'UPI',
    upi_txn_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Seed products (only if table is empty)
INSERT INTO products (name, description, price, image_url, category)
SELECT * FROM (VALUES
    ('Classic Black Tee', 'Premium cotton black t-shirt with signature logo', 2499, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Black+Tee', 'T-Shirts'),
    ('Dark Hoodie', 'Oversized fleece hoodie with embroidered design', 4999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Dark+Hoodie', 'Hoodies'),
    ('Slim Fit Jeans', 'Stretch denim jeans in obsidian black', 3999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Slim+Jeans', 'Bottoms'),
    ('Leather Jacket', 'Genuine leather biker jacket with silver hardware', 12999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Leather+Jacket', 'Outerwear'),
    ('Graphic Hoodie', 'Heavyweight hoodie with gothic print', 5499, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Graphic+Hoodie', 'Hoodies'),
    ('Cargo Pants', 'Multi-pocket cargo pants in black ripstop', 3799, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Cargo+Pants', 'Bottoms'),
    ('Varsity Jacket', 'Wool varsity jacket with satin sleeves', 10999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Varsity+Jacket', 'Outerwear'),
    ('Chain Necklace', 'Silver-toned curb chain accessory', 1599, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Chain', 'Accessories'),
    ('Beanie Hat', 'Ribbed knit beanie with embroidered patch', 999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Beanie', 'Accessories'),
    ('Oversized Tee', 'Relaxed fit tee with back print', 2999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Oversized+Tee', 'T-Shirts')
) AS v
WHERE NOT EXISTS (SELECT 1 FROM products LIMIT 1);
