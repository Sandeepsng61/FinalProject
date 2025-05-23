from app import app, db

# Initialize database tables
with app.app_context():
    from models import User, Product, CartItem, WishlistItem, Order, OrderItem
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
