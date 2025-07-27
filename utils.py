# utils.py

import pymysql
import re
from datetime import datetime
import streamlit as st

# -------------------------------
# ⚙️ Database Configuration
# -------------------------------
class DBConfig:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'root'
    DB_NAME = 'medicare_db'

    @staticmethod
    def get_connection():
        """Create and return a new MySQL database connection."""
        return pymysql.connect(
            host=DBConfig.HOST,
            user=DBConfig.USER,
            password=DBConfig.PASSWORD,
            db=DBConfig.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

# -------------------------------
# 🔄 Low-level DB Operations
# -------------------------------
class DBHelper:
    @staticmethod
    def fetch_all(query, params=None):
        """Execute a SELECT query and return all results."""
        with DBConfig.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()

    @staticmethod
    def fetch_one(query, params=None):
        """Execute a SELECT query and return one result."""
        with DBConfig.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()

    @staticmethod
    def execute(query, params=None):
        """Execute an INSERT/UPDATE/DELETE query."""
        with DBConfig.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())

# -------------------------------
# 👤 User Management
# -------------------------------
class User:
    @staticmethod
    def load_users():
        """Load all users from the database."""
        users = DBHelper.fetch_all("SELECT * FROM users")
        return {u['username']: u for u in users}

    @staticmethod
    def save_users(user_data):
        """Insert or update user data in the database."""
        with DBConfig.get_connection() as conn:
            with conn.cursor() as cursor:
                for username, data in user_data.items():
                    cursor.execute("""
                        REPLACE INTO users (username, email, password, role)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        username,
                        data['email'],
                        data['password'],
                        data.get('role', 'user')
                    ))

# -------------------------------
# 💊 Medicine Management
# -------------------------------
class Medicine:
    @staticmethod
    def save_medicine(med):
        """Save or update a medicine record."""
        with DBConfig.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    REPLACE INTO medicines (
                        id, name, description, category, price, stock, expiry_date,
                        manufacturer, requires_prescription
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    med.get('id'),
                    med['name'],
                    med['description'],
                    med['category'],
                    med['price'],
                    med['stock'],
                    med['expiry_date'],
                    med['manufacturer'],
                    int(med.get('requires_prescription', False))
                ))

# -------------------------------
# 📦 Orders
# -------------------------------
class Order:
    @staticmethod
    def insert_order(order):
        """Insert a new order along with its items."""
        with DBConfig.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO orders (user, total, address, datetime)
                    VALUES (%s, %s, %s, %s)
                """, (
                    order['user'],
                    order['total'],
                    order['address'],
                    order['datetime']
                ))
                order_id = cursor.lastrowid

                for item in order['items']:
                    cursor.execute("""
                        INSERT INTO order_items (
                            order_id, medicine_id, medicine_name, qty, price, expiry_date
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        order_id,
                        item.get('id', 0),
                        item['name'],
                        item['qty'],
                        item['price'],
                        item.get('expiry_date')
                    ))
                return order_id

    @staticmethod
    def get_user_orders(username):
        """Get all orders for a specific user."""
        return DBHelper.fetch_all(
            "SELECT * FROM orders WHERE user=%s ORDER BY datetime DESC",
            (username,)
        )

# -------------------------------
# 💬 Consultations
# -------------------------------
class Consultation:
    @staticmethod
    def save(consultation):
        """Save a user consultation request."""
        with DBConfig.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO consultations (user, symptoms, preferred_time, datetime)
                    VALUES (%s, %s, %s, %s)
                """, (
                    consultation['user'],
                    consultation['symptoms'],
                    consultation['preferred_time'],
                    consultation['datetime']
                ))

    @staticmethod
    def get_user_consultations(username):
        """Get consultations for a single user."""
        return DBHelper.fetch_all(
            "SELECT * FROM consultations WHERE user=%s ORDER BY datetime DESC",
            (username,)
        )

    @staticmethod
    def load_all():
        """Return all consultations (admin only)."""
        return DBHelper.fetch_all(
            "SELECT * FROM consultations ORDER BY datetime DESC"
        )

# -------------------------------
# 📬 Validators
# -------------------------------
class Validator:
    @staticmethod
    def is_valid_email(email):
        """Validate email format."""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_password(password):
        """Enforce strong password rules."""
        if len(password) < 6:
            return False, "Password must be at least 6 characters."
        if not any(c.islower() for c in password):
            return False, "Password must contain a lowercase letter."
        if not any(c.isupper() for c in password):
            return False, "Password must contain an uppercase letter."
        if not any(c.isdigit() for c in password):
            return False, "Password must include at least 1 number."
        if not any(c in "!@#$%^&*()-_+=" for c in password):
            return False, "Password must include a special character (!@#$...)"
        return True, ""

# -------------------------------
# 🔁 Streamlit Helpers
# -------------------------------
class StreamlitHelper:
    @staticmethod
    def rerun(module):
        """Safely rerun Streamlit app."""
        try:
            module.rerun()
        except AttributeError:
            module.experimental_rerun()


# These lines allow older scripts with `from utils import insert_order` to still work
insert_order = Order.insert_order
get_orders = Order.get_user_orders
save_user_data = User.save_users
load_user_data = User.load_users
save_consultation = Consultation.save
get_consultations = Consultation.get_user_consultations
