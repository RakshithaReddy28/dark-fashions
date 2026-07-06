-- Dark Fashions Database Schema
-- Import this in MySQL Workbench: File > Open SQL Script > Run (Ctrl+Shift+Enter)

CREATE DATABASE IF NOT EXISTS dark_fashions
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE dark_fashions;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    image_url VARCHAR(500),
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    shipping_address TEXT,
    pincode VARCHAR(10),
    payment_method VARCHAR(50) DEFAULT 'UPI',
    upi_txn_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Seed data (10 products)
INSERT INTO products (name, description, price, image_url, category) VALUES
('Classic Black Tee', 'Premium cotton black t-shirt with signature logo', 2499, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Black+Tee', 'T-Shirts'),
('Dark Hoodie', 'Oversized fleece hoodie with embroidered design', 4999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Dark+Hoodie', 'Hoodies'),
('Slim Fit Jeans', 'Stretch denim jeans in obsidian black', 3999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Slim+Jeans', 'Bottoms'),
('Leather Jacket', 'Genuine leather biker jacket with silver hardware', 12999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Leather+Jacket', 'Outerwear'),
('Graphic Hoodie', 'Heavyweight hoodie with gothic print', 5499, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Graphic+Hoodie', 'Hoodies'),
('Cargo Pants', 'Multi-pocket cargo pants in black ripstop', 3799, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Cargo+Pants', 'Bottoms'),
('Varsity Jacket', 'Wool varsity jacket with satin sleeves', 10999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Varsity+Jacket', 'Outerwear'),
('Chain Necklace', 'Silver-toned curb chain accessory', 1599, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Chain', 'Accessories'),
('Beanie Hat', 'Ribbed knit beanie with embroidered patch', 999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Beanie', 'Accessories'),
('Oversized Tee', 'Relaxed fit tee with back print', 2999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Oversized+Tee', 'T-Shirts');
