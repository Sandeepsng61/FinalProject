import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db_url = os.environ.get("DATABASE_URL")

# Some platforms give "postgres://", but SQLAlchemy needs "postgresql://"
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://")

# If you're on Railway and facing SSL issues, comment out sslmode
# app.config['SQLALCHEMY_DATABASE_URI'] = db_url + "?sslmode=require"
app.config['SQLALCHEMY_DATABASE_URI'] = db_url  # Safe for Railway

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db.init_app(app)


# initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Create all database tables
with app.app_context():
    from models import User, Product, CartItem, WishlistItem, Order, OrderItem
    db.create_all()

# Register routes after all configurations
from routes import *
