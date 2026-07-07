# Dark Fashions

Premium streetwear e-commerce platform built with Flask and PostgreSQL.

## Features

- User Registration & Authentication
- Product Catalog with Categories
- Product Detail Pages
- Shopping Cart with Quantity Management
- Checkout with UPI / COD Payment Options
- Order History & Confirmation
- Admin Panel for Product Management
- Black & Gold Theme
- Responsive Design

## Tech Stack

- **Backend:** Python, Flask
- **Database:** PostgreSQL (Render)
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Render

## Live Demo

[https://dark-fashions.onrender.com](https://dark-fashions.onrender.com)

## Admin Access

- **URL:** `/admin/login`
- **Password:** `admin123`

## Local Development

```bash
# Clone the repository
git clone https://github.com/RakshithaReddy28/dark-fashions.git
cd dark-fashions

# Install dependencies
pip install -r requirements.txt

# Set database URL (or use default SQLite)
set DATABASE_URL=your_database_url

# Run the app
python app.py
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Flask secret key for sessions |

## Project Structure

```
dark-fashions/
├── app.py                 # Flask application
├── database.py            # Database connection & models
├── requirements.txt       # Python dependencies
├── Procfile               # Render deployment config
├── static/
│   ├── style.css          # Stylesheet
│   ├── logo.png           # Brand logo
│   └── products/          # Product images
└── templates/
    ├── base.html          # Layout template
    ├── register.html      # Registration page
    ├── login.html         # Login page
    ├── shop.html          # Product catalog
    ├── product.html       # Product detail
    ├── cart.html          # Shopping cart
    ├── checkout.html      # Checkout with UPI/COD
    ├── order_confirmation.html
    ├── orders.html        # Order history
    ├── admin*.html        # Admin panel
    └── admin_login.html   # Admin login
```
