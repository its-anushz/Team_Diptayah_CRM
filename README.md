# Team_Diptayah_CRM

This is a Django-based Customer Relationshop Management System (CRM) web application that allows administrators to manage customers, products, tags, and orders efficiently. It includes user authentication, role-based access control, and a clean dashboard interface.

## Features

- User registration and login
- Group-based permissions (Admin / Customer)
- Dashboard with customer and order overview
- CRUD operations for:
  - Customers
  - Products
  - Orders
- Search, filtering, and inline forms
- Success and error messages with redirect
- Admin-only access for management views
- Signals to auto-create a `Customer` profile upon new user registration


## Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Steps

# Step 1: Extract the project


# Step 2: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run migrations
python manage.py migrate

# Step 5: Create a superuser (admin)
python manage.py createsuperuser

# Step 6: Run the server
python manage.py runserver

## Technologies Used

- **Python** – Core programming language for backend logic
- **Django** – Web framework for building the CRM
- **SQLite3** – Lightweight relational database used for development
- **HTML/CSS (Bootstrap)** – Frontend styling and layout
- **JavaScript** – For interactivity and form enhancements
- **Django Signals and Messages Framework** – For automated processes and user feedback
