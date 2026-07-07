import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = "postgresql://admin:O2SHdt8IKm5DG86T7O5gCCI5C2903AFN@dpg-d9691quq1p3s73bn8ilg-a/dark_fashions"

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
            ('Classic Black Tee', 'Premium cotton black t-shirt with signature logo', 2499, '/static/products/black_tee.jpg', 'T-Shirts'),
            ('Dark Hoodie', 'Oversized fleece hoodie with embroidered design', 4999, '/static/products/dark_hoodie.webp', 'Hoodies'),
            ('Slim Fit Jeans', 'Stretch denim jeans in obsidian black', 3999, '/static/products/slim_fit_jeans.jpg', 'Bottoms'),
            ('Leather Jacket', 'Genuine leather biker jacket with silver hardware', 12999, '/static/products/leather_jacket.jpg', 'Outerwear'),
            ('Graphic Hoodie', 'Heavyweight hoodie with gothic print', 5499, '/static/products/graphic_hoodie.avif', 'Hoodies'),
            ('Cargo Pants', 'Multi-pocket cargo pants in black ripstop', 3799, '/static/products/cargo_pants.jpg', 'Bottoms'),
            ('Varsity Jacket', 'Wool varsity jacket with satin sleeves', 10999, '/static/products/varasity_jacket.webp', 'Outerwear'),
            ('Chain Necklace', 'Silver-toned curb chain accessory', 1599, '/static/products/chain.jpg', 'Accessories'),
            ('Beanie Hat', 'Ribbed knit beanie with embroidered patch', 999, '/static/products/hat.jpg', 'Accessories'),
            ('Oversized Tee', 'Relaxed fit tee with back print', 2999, '/static/products/oversized_tee.webp', 'T-Shirts'),
            ('Oversized Hoodie', 'Extra baggy fit hoodie with dropped shoulders', 4499, '/static/products/oversized_hoodie.avif', 'Hoodies'),
            ('Denim Jacket', 'Classic black denim jacket with silver buttons', 8999, '/static/products/denim_jacket.jpg', 'Outerwear'),
            ('Jogger Pants', 'Cuffed joggers with elastic waist and drawstring', 2999, '/static/products/joggers.jpg', 'Bottoms'),
            ('Graphic Tee', 'Oversized tee with skull graphic print', 2199, '/static/products/black_tee.jpg', 'T-Shirts'),
            ('Crewneck Sweater', 'Heavy knit crewneck sweater in charcoal', 3999, '/static/products/crew_neck.jpg', 'Sweaters'),
            ('Silver Chain', 'Premium iced-out pendant chain', 2999, '/static/products/chain.jpg', 'Accessories'),
            ('Cargo Joggers', 'Cargo joggers with side pockets and taper', 3499, '/static/products/joggers1.webp', 'Bottoms'),
            ('Corduroy Jacket', 'Brown corduroy overshirt jacket', 6999, '/static/products/denim_jacket.jpg', 'Outerwear'),
            ('Snapback Cap', 'Black snapback cap with gold embroidery', 1299, '/static/products/snap_cap.jpg', 'Accessories'),
            ('Turtleneck', 'Slim fit ribbed turtleneck in black', 2499, '/static/products/turtle_neck.jpg', 'T-Shirts'),
            ('Track Pants', 'Slim track pants with stripe detail', 2799, '/static/products/track_pants.jpg', 'Bottoms'),
            ('Bomber Jacket', 'Nylon bomber jacket with ribbed cuffs', 9999, '/static/products/bomber_jacket.jpg', 'Outerwear'),
            ('Ring Set', 'Silver-toned ring set (pack of 3)', 899, '/static/products/ring_set.webp', 'Accessories'),
            ('Half Zip Sweater', 'Half zip fleece sweater in black', 3499, '/static/products/half_zip.webp', 'Sweaters'),
            ('Wide Leg Pants', 'Wide leg trouser pants in black', 3299, '/static/products/track_pants.jpg', 'Bottoms'),
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
