# E Cart - Django-based E-commerce Application

E Cart is a Django-based E-commerce application designed to facilitate the buying and selling of products. The system includes three types of users: Admin, Dealers, and Customers.

## Features

### Admin
- **Dealer Management:**
  - Create and manage dealers.
  - View and edit dealer details.
- **Customer Management:**
  - View customer orders.
  - Manage customer accounts.

### Dealers
- **Product Management:**
  - Add new products to the catalog.
  - Edit and manage existing product details.
  
- **Order Tracking:**
  - Track orders for products they sell.

### Customers
- **Product Exploration:**
  - Browse through the product catalog.
  - View details of each product.

- **Shopping Cart:**
  - Add products to the shopping cart.
  - Remove products from the cart.

- **Order Placement:**
  - Place orders for selected products.
  - Choose between Cash on Delivery and Online Payment.

- **User Authentication:**
  - Customers can log in using OTP for a simplified authentication process.

## Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:roopeshkp34/E_cart.git
   cd E_cart
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```
6. Access the application at http://localhost:8000/admin_login/ to log in with the superuser account and start using the system.
