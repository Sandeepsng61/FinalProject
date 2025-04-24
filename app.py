import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# get database url from environment variable
db_url = os.environ.get("DATABASE_URL")

# Render may give "postgres://", SQLAlchemy needs "postgresql://"
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://")

# Add SSL requirement
app.config['SQLALCHEMY_DATABASE_URI'] = db_url + "?sslmode=require"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app
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
