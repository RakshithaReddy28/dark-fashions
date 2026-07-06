import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db, get_cursor, init_db, seed_products
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import functools
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/')
def home():
    return redirect(url_for('shop'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if not full_name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')

        db = get_db()
        cur = get_cursor(db)
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing = cur.fetchone()
        if existing:
            cur.close()
            db.close()
            flash('Email already registered. Please log in.', 'warning')
            return render_template('register.html')

        hashed = generate_password_hash(password)
        cur.execute("INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)",
                    (full_name, email, hashed))
        db.commit()
        cur.close()
        db.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash('Please fill in all fields.', 'danger')
            return render_template('login.html')

        db = get_db()
        cur = get_cursor(db)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('shop'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/shop')
@login_required
def shop():
    db = get_db()
    cur = get_cursor(db)
    cur.execute("SELECT * FROM products ORDER BY category, name")
    products = cur.fetchall()
    cur.close()
    db.close()
    return render_template('shop.html', products=products)

@app.route('/cart')
@login_required
def cart():
    db = get_db()
    cur = get_cursor(db)
    cur.execute('''
        SELECT c.id, c.quantity, p.id as product_id, p.name, p.price, p.image_url
        FROM cart c JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    ''', (session['user_id'],))
    items = cur.fetchall()
    total = sum(item['price'] * item['quantity'] for item in items)
    cur.close()
    db.close()
    return render_template('cart.html', items=items, total=total)

@app.route('/product/<int:product_id>')
@login_required
def product_detail(product_id):
    db = get_db()
    cur = get_cursor(db)
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    if not product:
        cur.close()
        db.close()
        flash('Product not found.', 'danger')
        return redirect(url_for('shop'))
    cur.execute("SELECT * FROM products WHERE category = %s AND id != %s ORDER BY RANDOM() LIMIT 4",
                (product['category'], product_id))
    related = cur.fetchall()
    cur.close()
    db.close()
    return render_template('product.html', product=product, related=related)

@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    db = get_db()
    cur = get_cursor(db)
    cur.execute(
        "SELECT id, quantity FROM cart WHERE user_id = %s AND product_id = %s",
        (session['user_id'], product_id)
    )
    existing = cur.fetchone()
    if existing:
        cur.execute("UPDATE cart SET quantity = quantity + %s WHERE id = %s",
                    (quantity, existing['id']))
    else:
        cur.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                    (session['user_id'], product_id, quantity))
    db.commit()
    cur.close()
    db.close()
    flash('Item added to cart!', 'success')
    return redirect(url_for('shop'))

@app.route('/add-to-cart-ajax', methods=['POST'])
@login_required
def add_to_cart_ajax():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    db = get_db()
    cur = get_cursor(db)
    cur.execute(
        "SELECT id, quantity FROM cart WHERE user_id = %s AND product_id = %s",
        (session['user_id'], product_id)
    )
    existing = cur.fetchone()
    if existing:
        cur.execute("UPDATE cart SET quantity = quantity + %s WHERE id = %s",
                    (quantity, existing['id']))
    else:
        cur.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                    (session['user_id'], product_id, quantity))
    db.commit()
    cur.close()
    db.close()
    return {'success': True}

@app.route('/update-cart', methods=['POST'])
@login_required
def update_cart():
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 1))
    if quantity < 1:
        quantity = 1
    db = get_db()
    cur = get_cursor(db)
    cur.execute("UPDATE cart SET quantity = %s WHERE id = %s AND user_id = %s",
               (quantity, item_id, session['user_id']))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('cart'))

@app.route('/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    item_id = request.form.get('item_id')
    db = get_db()
    cur = get_cursor(db)
    cur.execute("DELETE FROM cart WHERE id = %s AND user_id = %s",
               (item_id, session['user_id']))
    db.commit()
    cur.close()
    db.close()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    db = get_db()
    cur = get_cursor(db)
    cur.execute('''
        SELECT c.quantity, p.id as product_id, p.name, p.price
        FROM cart c JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    ''', (session['user_id'],))
    items = cur.fetchall()

    if not items:
        cur.close()
        db.close()
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('shop'))

    total = sum(item['price'] * item['quantity'] for item in items)

    if request.method == 'POST':
        address = request.form['address']
        pincode = request.form['pincode']
        payment_method = request.form.get('payment_method', 'UPI')
        upi_txn_id = request.form.get('upi_txn_id', '')

        if not address:
            cur.close()
            db.close()
            flash('Please enter your shipping address.', 'danger')
            return render_template('checkout.html', items=items, total=total)

        cur.execute("INSERT INTO orders (user_id, total_amount, shipping_address, pincode, payment_method, upi_txn_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                    (session['user_id'], total, address, pincode, payment_method, upi_txn_id))
        order_id = cur.fetchone()[0]

        for item in items:
            cur.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                       (order_id, item['product_id'], item['quantity'], item['price']))

        cur.execute("DELETE FROM cart WHERE user_id = %s", (session['user_id'],))
        db.commit()
        cur.close()
        db.close()
        flash('Order placed successfully! Thank you for your purchase.', 'success')
        return redirect(url_for('order_confirmation', order_id=order_id))

    cur.close()
    db.close()
    return render_template('checkout.html', items=items, total=total)

@app.route('/order-confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    db = get_db()
    cur = get_cursor(db)
    cur.execute("SELECT * FROM orders WHERE id = %s AND user_id = %s", (order_id, session['user_id']))
    order = cur.fetchone()
    if not order:
        cur.close()
        db.close()
        flash('Order not found.', 'danger')
        return redirect(url_for('orders'))
    cur.execute('''
        SELECT oi.quantity, oi.price, p.name
        FROM order_items oi JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
    ''', (order_id,))
    items = cur.fetchall()
    cur.close()
    db.close()
    return render_template('order_confirmation.html', order=order, items=items)

@app.route('/orders')
@login_required
def orders():
    db = get_db()
    cur = get_cursor(db)
    cur.execute('''
        SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC
    ''', (session['user_id'],))
    orders = cur.fetchall()
    order_items = {}
    for order in orders:
        cur.execute('''
            SELECT oi.quantity, oi.price, p.name
            FROM order_items oi JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        ''', (order['id'],))
        order_items[order['id']] = cur.fetchall()
    cur.close()
    db.close()
    return render_template('orders.html', orders=orders, order_items=order_items)

ADMIN_PASSWORD = 'admin123'

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('is_admin'):
            flash('Admin access required.', 'warning')
            return redirect(url_for('admin_login'))
        return view(**kwargs)
    return wrapped_view

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin'))
        flash('Wrong password.', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('shop'))

@app.route('/admin')
@admin_required
def admin():
    db = get_db()
    cur = get_cursor(db)
    cur.execute("SELECT * FROM products ORDER BY id")
    products = cur.fetchall()
    cur.close()
    db.close()
    return render_template('admin.html', products=products)

@app.route('/admin/add', methods=['GET', 'POST'])
@admin_required
def admin_add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        image_url = 'https://placehold.co/300x400/1a1a1a/ffffff?text=New'

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join('static/products', filename)
                file.save(os.path.join(app.root_path, filepath))
                image_url = url_for('static', filename=f'products/{filename}')

        db = get_db()
        cur = get_cursor(db)
        cur.execute("INSERT INTO products (name, description, price, image_url, category) VALUES (%s, %s, %s, %s, %s)",
                    (name, description, price, image_url, category))
        db.commit()
        cur.close()
        db.close()
        flash('Product added!', 'success')
        return redirect(url_for('admin'))

    return render_template('admin_add.html')

@app.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(product_id):
    db = get_db()
    cur = get_cursor(db)
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()

    if not product:
        cur.close()
        db.close()
        flash('Product not found.', 'danger')
        return redirect(url_for('admin'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']

        image_url = product['image_url']
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join('static/products', filename)
                file.save(os.path.join(app.root_path, filepath))
                image_url = url_for('static', filename=f'products/{filename}')

        cur.execute("UPDATE products SET name=%s, description=%s, price=%s, category=%s, image_url=%s WHERE id=%s",
                    (name, description, price, category, image_url, product_id))
        db.commit()
        cur.close()
        db.close()
        flash('Product updated!', 'success')
        return redirect(url_for('admin'))

    cur.close()
    db.close()
    return render_template('admin_edit.html', product=product)

@app.route('/admin/delete/<int:product_id>')
@admin_required
def admin_delete(product_id):
    db = get_db()
    cur = get_cursor(db)
    cur.execute("DELETE FROM cart WHERE product_id = %s", (product_id,))
    cur.execute("DELETE FROM order_items WHERE product_id = %s", (product_id,))
    cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
    db.commit()
    cur.close()
    db.close()
    flash('Product deleted.', 'info')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    seed_products()
    app.run(host='0.0.0.0', port=5000, debug=True)
