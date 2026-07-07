import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ.get('DATABASE_URL', "postgresql://postgres:Rakshitharedddy%4028@db.buwkgovwcbrumamysbvu.supabase.co:5432/postgres?sslmode=require")

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def get_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")
    tables = [
        """CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            image_url VARCHAR(500),
            category VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS cart (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
            quantity INT NOT NULL DEFAULT 1
        )""",
        """CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            total_amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            shipping_address TEXT,
            pincode VARCHAR(10),
            payment_method VARCHAR(50) DEFAULT 'UPI',
            upi_txn_id VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
            product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
            quantity INT NOT NULL,
            price DECIMAL(10,2) NOT NULL
        )""",
    ]
    for t in tables:
        cur.execute(t)
    conn.commit()
    cur.close()
    conn.close()

def seed_products():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM products")
    count = cur.fetchone()[0]
    if count == 0:
        products = [
            ('Classic Black Tee', 'Premium cotton black t-shirt with signature logo', 2499, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Black+Tee', 'T-Shirts'),
            ('Dark Hoodie', 'Oversized fleece hoodie with embroidered design', 4999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Dark+Hoodie', 'Hoodies'),
            ('Slim Fit Jeans', 'Stretch denim jeans in obsidian black', 3999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Slim+Jeans', 'Bottoms'),
            ('Leather Jacket', 'Genuine leather biker jacket with silver hardware', 12999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Leather+Jacket', 'Outerwear'),
            ('Graphic Hoodie', 'Heavyweight hoodie with gothic print', 5499, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Graphic+Hoodie', 'Hoodies'),
            ('Cargo Pants', 'Multi-pocket cargo pants in black ripstop', 3799, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Cargo+Pants', 'Bottoms'),
            ('Varsity Jacket', 'Wool varsity jacket with satin sleeves', 10999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Varsity+Jacket', 'Outerwear'),
            ('Chain Necklace', 'Silver-toned curb chain accessory', 1599, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Chain', 'Accessories'),
            ('Beanie Hat', 'Ribbed knit beanie with embroidered patch', 999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Beanie', 'Accessories'),
            ('Oversized Tee', 'Relaxed fit tee with back print', 2999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Oversized+Tee', 'T-Shirts'),
            ('Oversized Hoodie', 'Extra baggy fit hoodie with dropped shoulders', 4499, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Oversized+Hoodie', 'Hoodies'),
            ('Denim Jacket', 'Classic black denim jacket with silver buttons', 8999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Denim+Jacket', 'Outerwear'),
            ('Jogger Pants', 'Cuffed joggers with elastic waist and drawstring', 2999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Jogger+Pants', 'Bottoms'),
            ('Graphic Tee', 'Oversized tee with skull graphic print', 2199, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Graphic+Tee', 'T-Shirts'),
            ('Crewneck Sweater', 'Heavy knit crewneck sweater in charcoal', 3999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Crewneck', 'Sweaters'),
            ('Silver Chain', 'Premium iced-out pendant chain', 2999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Silver+Chain', 'Accessories'),
            ('Cargo Joggers', 'Cargo joggers with side pockets and taper', 3499, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Cargo+Joggers', 'Bottoms'),
            ('Corduroy Jacket', 'Brown corduroy overshirt jacket', 6999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Corduroy+Jacket', 'Outerwear'),
            ('Snapback Cap', 'Black snapback cap with gold embroidery', 1299, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Snapback', 'Accessories'),
            ('Turtleneck', 'Slim fit ribbed turtleneck in black', 2499, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Turtleneck', 'T-Shirts'),
            ('Track Pants', 'Slim track pants with stripe detail', 2799, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Track+Pants', 'Bottoms'),
            ('Bomber Jacket', 'Nylon bomber jacket with ribbed cuffs', 9999, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Bomber+Jacket', 'Outerwear'),
            ('Ring Set', 'Silver-toned ring set (pack of 3)', 899, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Ring+Set', 'Accessories'),
            ('Half Zip Sweater', 'Half zip fleece sweater in black', 3499, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Half+Zip', 'Sweaters'),
            ('Wide Leg Pants', 'Wide leg trouser pants in black', 3299, 'https://placehold.co/300x400/1a1a1a/ffffff?text=Wide+Leg+Pants', 'Bottoms'),
        ]
        for p in products:
            cur.execute("INSERT INTO products (name, description, price, image_url, category) VALUES (%s, %s, %s, %s, %s)", p)
        conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    init_db()
    seed_products()
    print("Supabase database initialized and seeded successfully.")
