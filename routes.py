import os
import json
import uuid
from datetime import datetime
from functools import wraps

from flask import render_template, url_for, flash, redirect, request, session, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db
from forms import LoginForm, RegistrationForm, CheckoutForm, PaymentForm, SearchForm, AdminLoginForm
from models import User, Product, CartItem, Order, OrderItem, WishlistItem

# Helper functions
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
def get_cart_items():
    """Get cart items for current user with product details"""
    if current_user.is_authenticated:
        # Get cart items with joined product data
        cart_items = db.session.query(CartItem, Product).join(
            Product, CartItem.product_id == Product.id
        ).filter(CartItem.user_id == current_user.id).all()
        
        # Format as a list of dictionaries
        cart = []
        total = 0
        
        for cart_item, product in cart_items:
            item_total = product.price * cart_item.quantity
            total += item_total
            
            cart.append({
                'id': cart_item.id,
                'product': product,
                'quantity': cart_item.quantity,
                'item_total': item_total
            })
        
        return cart, total
    
    return [], 0

def get_cart_count():
    """Get number of items in cart"""
    if current_user.is_authenticated:
        return CartItem.query.filter_by(user_id=current_user.id).count()
    return 0

@app.context_processor
def inject_cart_count():
    """Inject cart count to all templates"""
    return dict(cart_count=get_cart_count())

@app.route('/')
def index():
    """Home page route"""
    featured_products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    return render_template('index.html', featured_products=featured_products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please use a different one.', 'danger')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard page"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', orders=orders, wishlist_items=wishlist_items)

@app.route('/components')
def components():
    """Components listing page"""
    category = request.args.get('category', 'all')
    component_categories = ['cpu', 'motherboard', 'ram', 'storage', 'gpu', 'psu', 'case', 'cooling']
    
    if category != 'all' and category in component_categories:
        products = Product.query.filter_by(category=category).all()
    else:
        # Get all components
        products = Product.query.filter(Product.category.in_(component_categories)).all()
    
    return render_template('components.html', products=products, category=category)

@app.route('/intel-pcs')
def intel_pcs():
    """Intel PCs listing page"""
    products = Product.query.filter(Product.name.like('%Intel%')).all()
    return render_template('intel_pcs.html', products=products)

@app.route('/amd-pcs')
def amd_pcs():
    """AMD PCs listing page"""
    products = Product.query.filter(Product.name.like('%AMD%')).all()
    return render_template('amd_pcs.html', products=products)

@app.route('/monitors')
def monitors():
    """Monitors listing page"""
    products = Product.query.filter_by(category='monitor').all()
    return render_template('monitors.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = Product.query.get_or_404(product_id)
    
    # Get related products
    related_products = Product.query.filter_by(category=product.category).filter(Product.id != product.id).limit(4).all()
    
    return render_template('product_detail.html', product=product, related_products=related_products)

@app.route('/pc-builder')
def pc_builder():
    """PC Builder page"""
    categories = ['cpu', 'motherboard', 'ram', 'storage', 'gpu', 'psu', 'case', 'cooling']
    components = {}
    
    for category in categories:
        components[category] = Product.query.filter_by(category=category).all()
    
    return render_template('pc_builder.html', categories=categories, components=components)

@app.route('/search')
def search():
    """Search results page"""
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('index'))
    
    # Search in product name and description
    products = Product.query.filter(
        (Product.name.ilike(f'%{query}%')) | 
        (Product.description.ilike(f'%{query}%'))
    ).all()
    
    return render_template('search_results.html', products=products, query=query)

@app.route('/cart')
@login_required
def view_cart():
    """View cart page"""
    cart, total = get_cart_items()
    return render_template('view_cart.html', cart=cart, total=total)

@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    """Add product to cart"""
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    if not product_id:
        flash('No product has been selected.', 'danger')
        return redirect(request.referrer or url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    
    # Check if product is in stock
    if product.stock < quantity:
        flash('Sorry, this product is either out of stock or the requested quantity is not available.', 'danger')
        return redirect(request.referrer or url_for('index'))
    
    # Check if product already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        # Update quantity
        cart_item.quantity += quantity
    else:
        # Add new item to cart
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} has been added to your cart.', 'success')
    
    # Redirect back to previous page or cart
    return redirect(request.referrer or url_for('view_cart'))

@app.route('/add-pc-to-cart', methods=['POST'])
@login_required
def add_pc_to_cart():
    """Add all PC components to cart"""
    categories = ['cpu', 'motherboard', 'ram', 'storage', 'gpu', 'psu', 'case', 'cooling']
    added_products = []
    
    for category in categories:
        product_id = request.form.get(f'{category}_id')
        if product_id:
            product = Product.query.get(product_id)
            
            if product:
                # Check if product already in cart
                cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
                
                if cart_item:
                    # Update quantity
                    cart_item.quantity += 1
                else:
                    # Add new item to cart
                    cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
                    db.session.add(cart_item)
                
                added_products.append(product.name)
    
    if added_products:
        db.session.commit()
        flash(f'{len(added_products)} Components have been added to your cart.', 'success')
    else:
        flash('No component selected. Please choose at least one component.', 'warning')
    
    return redirect(url_for('view_cart'))

@app.route('/update-cart', methods=['POST'])
@login_required
def update_cart():
    """Update cart item quantity"""
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    if not product_id:
        return jsonify({'error': 'No product selected.'}), 400
    
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if not cart_item:
        return jsonify({'error': 'Item not found in cart.'}), 404
    
    # Check stock
    if quantity > cart_item.product.stock:
        return jsonify({'error': f'Only {cart_item.product.stock} available in stock.'}), 400
    
    cart_item.quantity = quantity
    db.session.commit()
    
    # Get updated cart total
    cart, total = get_cart_items()
    
    return jsonify({
        'success': True,
        'message': 'Cart updated.',
        'item_total': cart_item.product.price * quantity,
        'cart_total': total
    })

@app.route('/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    """Remove item from cart"""
    product_id = request.form.get('product_id')
    
    if not product_id:
        flash('No product selected.', 'danger')
        return redirect(url_for('view_cart'))
    
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart.', 'success')
    
    return redirect(url_for('view_cart'))

@app.route('/clear-cart')
@login_required
def clear_cart():
    """Clear all items from cart"""
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('Your cart has been cleared.', 'info')
    return redirect(url_for('view_cart'))

@app.route('/wishlist')
@login_required
def wishlist():
    """View wishlist page"""
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/add-to-wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    """Add product to wishlist"""
    product_id = request.form.get('product_id')
    
    if not product_id:
        flash('No product selected.', 'danger')
        return redirect(request.referrer or url_for('index'))
    
    # Check if product already in wishlist
    existing_item = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if existing_item:
        flash('This product is already in your wishlist.', 'info')
    else:
        wishlist_item = WishlistItem(user_id=current_user.id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash('Product added to your wishlist.', 'success')
    
    return redirect(request.referrer or url_for('index'))

@app.route('/remove-from-wishlist', methods=['POST'])
@login_required
def remove_from_wishlist():
    """Remove item from wishlist"""
    product_id = request.form.get('product_id')
    
    if not product_id:
        flash('No product selected.', 'danger')
        return redirect(url_for('wishlist'))
    
    wishlist_item = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Item removed from wishlist.', 'success')
    
    return redirect(url_for('wishlist'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    cart, total = get_cart_items()
    
    if not cart:
        flash('Your cart is empty. Add some products before checkout.', 'info')
        return redirect(url_for('index'))
    
    form = CheckoutForm()
    
    # Pre-fill form with user data
    if request.method == 'GET':
        form.email.data = current_user.email
    
    if form.validate_on_submit():
        # Save checkout info to session
        session['checkout_info'] = {
            'full_name': form.full_name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'address': form.address.data,
            'city': form.city.data,
            'state': form.state.data,
            'zipcode': form.zipcode.data,
            'country': form.country.data,
            'payment_method': form.payment_method.data
        }
        
        return redirect(url_for('payment'))
    
    return render_template('checkout.html', form=form, cart=cart, total=total)

@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    """Payment page"""
    # Check if checkout info exists
    if 'checkout_info' not in session:
        flash('Please complete the checkout process first.', 'warning')
        return redirect(url_for('checkout'))
    
    cart, total = get_cart_items()
    
    if not cart:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('index'))
    
    form = PaymentForm()
    
    # Get checkout info
    checkout_info = session.get('checkout_info', {})
    
    # For COD, don't validate card fields
    if checkout_info.get('payment_method') == 'cod' and request.method == 'POST':
        # Skip validation for COD
        create_order = True
    else:
        create_order = form.validate_on_submit()
    
    if create_order:
        # Create order
        checkout_info = session['checkout_info']
        
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            status='pending',
            shipping_address=checkout_info['address'],
            shipping_city=checkout_info['city'],
            shipping_state=checkout_info['state'],
            shipping_country=checkout_info['country'],
            shipping_zipcode=checkout_info['zipcode'],
            contact_phone=checkout_info['phone'],
            payment_method=checkout_info['payment_method'],
            transaction_id=f'TXID-{uuid.uuid4().hex[:8].upper()}'
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID without committing
        
        # Add order items
        for item in cart:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['product'].price
            )
            
            # Update product stock
            product = item['product']
            product.stock -= item['quantity']
            
            db.session.add(order_item)
        
        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        
        # Clear checkout info
        session.pop('checkout_info', None)
        
        db.session.commit()
        
        # Store order ID for confirmation page
        session['last_order_id'] = order.id
        
        flash('Payment successful! Your order has been placed.', 'success')
        return redirect(url_for('order_confirmation'))
    
    return render_template('payment.html', form=form, cart=cart, total=total, 
                          checkout_info=session['checkout_info'])

@app.route('/order-confirmation')
@login_required
def order_confirmation():
    """Order confirmation page"""
    # Check if last order exists
    if 'last_order_id' not in session:
        flash('No recent order found.', 'warning')
        return redirect(url_for('index'))
    
    order_id = session['last_order_id']
    order = Order.query.get_or_404(order_id)
    
    # Verify order belongs to current user
    if order.user_id != current_user.id:
        abort(403)
    
    # Get order items
    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    
    # Clear last order ID from session
    session.pop('last_order_id', None)
    
    return render_template('order_confirmation.html', order=order, order_items=order_items)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin_panel'))
    
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data) and user.is_admin:
            login_user(user)
            return redirect(url_for('admin_panel'))
        else:
            flash('Invalid credentials or you do not have admin privileges.', 'danger')
    
    return render_template('admin_login.html', form=form)

@app.route('/admin-panel')
@login_required
@admin_required
def admin_panel():
    """Admin panel page"""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    users = User.query.all()
    products = Product.query.all()
    
    return render_template('admin_panel.html', orders=orders, users=users, products=products)
    
@app.route('/admin/add-product', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_product():
    """Add or edit product page"""
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        
        # Parse specs JSON
        specs = {}
        try:
            specs_text = request.form.get('specs', '{}')
            if specs_text.strip():
                specs = json.loads(specs_text)
        except json.JSONDecodeError:
            flash('Invalid JSON format in specs. Please check the format.', 'danger')
            return redirect(url_for('admin_add_product'))
        
        # Set default image URL if none provided
        image_url = request.form.get('image_url', '')
        if not image_url:
            category = request.form.get('category')
            name = request.form.get('name')
            image_url = f'https://via.placeholder.com/300x300.png?text={name.replace(" ", "+")}'
            
        # Create or update product
        if product_id:
            # Update existing product
            product = Product.query.get_or_404(product_id)
            product.name = request.form.get('name')
            product.category = request.form.get('category')
            product.description = request.form.get('description')
            product.price = float(request.form.get('price'))
            product.stock = int(request.form.get('stock', 0))
            product.image_url = image_url
            product.specs = specs
            
            db.session.commit()
            flash(f'Product "{product.name}" updated successfully!', 'success')
        else:
            # Create new product
            product = Product(
                name=request.form.get('name'),
                category=request.form.get('category'),
                description=request.form.get('description'),
                price=float(request.form.get('price')),
                stock=int(request.form.get('stock', 0)),
                image_url=image_url,
                specs=specs
            )
            
            db.session.add(product)
            db.session.commit()
            flash(f'Product "{product.name}" added successfully!', 'success')
            
        return redirect(url_for('admin_panel'))
        
    # GET request - show form
    product_id = request.args.get('id')
    product = None
    
    if product_id:
        product = Product.query.get_or_404(product_id)
    
    return render_template('admin_product_form.html', product=product)

@app.route('/admin/order/<int:order_id>')
@login_required
@admin_required
def admin_order_detail(order_id):
    """Admin order detail page"""
    order = Order.query.get_or_404(order_id)
    order_items = OrderItem.query.filter_by(order_id=order.id).all()
    
    return render_template('admin_order_detail.html', order=order, order_items=order_items)

@app.route('/admin/update-order-status/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def admin_update_order_status(order_id):
    """Update order status"""
    status = request.form.get('status')
    
    if not status:
        flash('No status provided.', 'danger')
        return redirect(url_for('admin_order_detail', order_id=order_id))
    
    order = Order.query.get_or_404(order_id)
    order.status = status
    db.session.commit()
    
    flash(f'Order status updated to {status}.', 'success')
    return redirect(url_for('admin_order_detail', order_id=order_id))

# API Routes for PC Builder
@app.route('/api/check-compatibility', methods=['POST'])
def check_compatibility():
    """API to check component compatibility"""
    components = request.json
    
    # Example compatibility check - this would be more complex in real application
    compatibility_issues = []
    
    # Check CPU and motherboard compatibility
    if 'cpu' in components and 'motherboard' in components:
        cpu_id = components['cpu']
        motherboard_id = components['motherboard']
        
        cpu = Product.query.get(cpu_id)
        motherboard = Product.query.get(motherboard_id)
        
        if cpu and motherboard and cpu.specs and motherboard.specs:
            # Check socket compatibility
            cpu_socket = cpu.specs.get('socket')
            motherboard_socket = motherboard.specs.get('socket')
            
            if cpu_socket and motherboard_socket and cpu_socket != motherboard_socket:
                compatibility_issues.append(f"CPU socket ({cpu_socket}) is not compatible with motherboard socket ({motherboard_socket}).")
    
    # Example power check
    if 'psu' in components and components['psu']:
        estimated_wattage = 0
        
        # Calculate based on components
        if 'cpu' in components and components['cpu']:
            cpu = Product.query.get(components['cpu'])
            if cpu and cpu.specs and 'tdp' in cpu.specs:
                estimated_wattage += int(cpu.specs['tdp'])
            else:
                estimated_wattage += 65  # Default CPU power
                
        if 'gpu' in components and components['gpu']:
            gpu = Product.query.get(components['gpu'])
            if gpu and gpu.specs and 'tdp' in gpu.specs:
                estimated_wattage += int(gpu.specs['tdp'])
            else:
                estimated_wattage += 150  # Default GPU power
        
        # Add base system power
        estimated_wattage += 100
        
        # Get PSU wattage
        psu = Product.query.get(components['psu'])
        if psu and psu.specs and 'wattage' in psu.specs:
            psu_wattage = int(psu.specs['wattage'])
            
            if estimated_wattage > psu_wattage:
                compatibility_issues.append(f"Your build may require {estimated_wattage}W but selected PSU is only {psu_wattage}W.")
    
    # Initialize estimated_wattage with default value
    estimated_wattage = locals().get('estimated_wattage', 0)
        
    return jsonify({
        'compatible': len(compatibility_issues) == 0,
        'estimated_wattage': estimated_wattage,
        'issues': compatibility_issues
    })

@app.route('/admin/seed-data')
@login_required
@admin_required
def seed_data():
    """Seed the database with sample products - for development only"""
    # Create admin user if doesn't exist
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Sample categories and products
    categories = {
        'cpu': [
            {
                'name': 'Intel Core i9-12900K',
                'description': 'Intel Core i9-12900K Desktop Processor 16 Cores up to 5.2 GHz Unlocked',
                'price': 44999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=Intel+i9+12900K',
                'stock': 15,
                'specs': {
                    'processor_family': 'i9',
                    'cores': '16 cores (8P+8E)',
                    'threads': '24',
                    'socket': 'LGA1700',
                    'base_clock': '3.2 GHz',
                    'boost_clock': '5.2 GHz',
                    'tdp': '125W',
                    'architecture': 'Alder Lake'
                }
            },
            {
                'name': 'Intel Core i7-12700K',
                'description': 'Intel Core i7-12700K Desktop Processor 12 Cores up to 5.0 GHz Unlocked',
                'price': 34999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=Intel+i7+12700K',
                'stock': 20,
                'specs': {
                    'processor_family': 'i7',
                    'cores': '12 cores (8P+4E)',
                    'threads': '20',
                    'socket': 'LGA1700',
                    'base_clock': '3.6 GHz',
                    'boost_clock': '5.0 GHz',
                    'tdp': '125W',
                    'architecture': 'Alder Lake'
                }
            },
            {
                'name': 'AMD Ryzen 9 5900X',
                'description': 'AMD Ryzen 9 5900X Desktop Processor 12 Cores up to 4.8 GHz Unlocked',
                'price': 39999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=AMD+Ryzen+9+5900X',
                'stock': 10,
                'specs': {
                    'processor_family': 'Ryzen 9',
                    'cores': '12',
                    'threads': '24',
                    'socket': 'AM4',
                    'base_clock': '3.7 GHz',
                    'boost_clock': '4.8 GHz',
                    'tdp': '105W',
                    'architecture': 'Zen 3'
                }
            }
        ],
        'motherboard': [
            {
                'name': 'ASUS ROG Maximus Z690 Hero',
                'description': 'ASUS ROG Maximus Z690 Hero LGA1700 Motherboard for Intel 12th Gen CPUs',
                'price': 49999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=ASUS+ROG+Maximus+Z690',
                'stock': 8,
                'specs': {
                    'socket': 'LGA1700',
                    'chipset': 'Z690',
                    'form_factor': 'ATX',
                    'memory_slots': '4',
                    'max_memory': '128GB DDR5',
                    'pcie_slots': '3 x PCIe 5.0/4.0',
                    'm2_slots': '5 x M.2'
                }
            }
        ],
        'gpu': [
            {
                'name': 'NVIDIA GeForce RTX 3080 Ti',
                'description': 'NVIDIA GeForce RTX 3080 Ti 12GB GDDR6X Graphics Card',
                'price': 119999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=RTX+3080+Ti',
                'stock': 5,
                'specs': {
                    'memory': '12GB GDDR6X',
                    'boost_clock': '1.67 GHz',
                    'tdp': '350W',
                    'cuda_cores': '10240',
                    'rt_cores': '80',
                    'tensor_cores': '320'
                }
            }
        ],
        'ram': [
            {
                'name': 'Corsair Vengeance RGB Pro 32GB',
                'description': 'Corsair Vengeance RGB Pro 32GB (2x16GB) DDR4 3600MHz Desktop Memory',
                'price': 14999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=Corsair+Vengeance+RGB',
                'stock': 25,
                'specs': {
                    'capacity': '32GB (2x16GB)',
                    'speed': 'DDR4-3600MHz',
                    'cas_latency': 'CL18',
                    'voltage': '1.35V',
                    'rgb': 'Yes'
                }
            }
        ],
        'storage': [
            {
                'name': 'Samsung 970 EVO Plus 1TB',
                'description': 'Samsung 970 EVO Plus 1TB PCIe NVMe M.2 Internal SSD',
                'price': 8999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=Samsung+970+EVO+Plus',
                'stock': 30,
                'specs': {
                    'capacity': '1TB',
                    'type': 'NVMe SSD',
                    'interface': 'PCIe 3.0 x4',
                    'form_factor': 'M.2 2280',
                    'sequential_read': '3500 MB/s',
                    'sequential_write': '3300 MB/s'
                }
            }
        ],
        'psu': [
            {
                'name': 'EVGA SuperNOVA 850 G5',
                'description': 'EVGA SuperNOVA 850 G5, 80 Plus Gold 850W, Fully Modular Power Supply',
                'price': 12999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=EVGA+SuperNOVA+850',
                'stock': 15,
                'specs': {
                    'wattage': '850',
                    'certification': '80+ Gold',
                    'modularity': 'Fully Modular',
                    'fan_size': '135mm',
                    'efficiency': '90%',
                    'protection': 'OVP, UVP, OCP, OPP, SCP, OTP'
                }
            }
        ],
        'case': [
            {
                'name': 'NZXT H510 Elite',
                'description': 'NZXT H510 Elite - Premium Mid-Tower ATX Case with Tempered Glass',
                'price': 9999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=NZXT+H510+Elite',
                'stock': 10,
                'specs': {
                    'form_factor': 'Mid Tower',
                    'motherboard_support': 'Mini-ITX, MicroATX, ATX',
                    'dimensions': '210mm x 460mm x 428mm',
                    'material': 'Steel, Tempered Glass',
                    'expansion_slots': '7',
                    'included_fans': '2 x 140mm front, 1 x 120mm top, 1 x 120mm rear'
                }
            }
        ],
        'cooling': [
            {
                'name': 'NZXT Kraken X63',
                'description': 'NZXT Kraken X63 280mm AIO Liquid CPU Cooler',
                'price': 13999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=NZXT+Kraken+X63',
                'stock': 12,
                'specs': {
                    'type': 'Liquid Cooler',
                    'radiator_size': '280mm',
                    'fans': '2 x 140mm Aer P',
                    'socket_support': 'Intel LGA 1700, 1200, 1151, AMD AM4',
                    'rgb': 'Yes',
                    'fan_speed': '500-2000 RPM'
                }
            }
        ],
        'monitor': [
            {
                'name': 'LG 27GL850-B UltraGear',
                'description': 'LG 27GL850-B 27" UltraGear QHD IPS 1ms 144Hz Gaming Monitor',
                'price': 29999.99,
                'image_url': 'https://via.placeholder.com/300x300.png?text=LG+UltraGear',
                'stock': 8,
                'specs': {
                    'size': '27"',
                    'resolution': '2560 x 1440 (QHD)',
                    'panel_type': 'IPS',
                    'refresh_rate': '144Hz',
                    'response_time': '1ms',
                    'adaptive_sync': 'G-Sync Compatible, FreeSync',
                    'hdr': 'HDR10'
                }
            }
        ]
    }
    
    # Add products if not exists
    for category, products in categories.items():
        for product_data in products:
            existing = Product.query.filter_by(name=product_data['name']).first()
            if not existing:
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    category=category,
                    image_url=product_data['image_url'],
                    stock=product_data['stock'],
                    specs=product_data['specs']
                )
                db.session.add(product)
    
    # Add prebuilt PCs
    prebuilt_pcs = [
        {
            'name': 'SS Gaming Beast - Intel Edition',
            'description': 'High performance gaming PC with Intel Core i9 and RTX 3080 Ti',
            'price': 199999.99,
            'category': 'prebuilt',
            'image_url': 'https://via.placeholder.com/300x300.png?text=Gaming+Beast+Intel',
            'stock': 3,
            'specs': {
                'processor': 'Intel Core i9-12900K',
                'processor_family': 'i9',
                'motherboard': 'ASUS ROG Maximus Z690 Hero',
                'ram': '32GB DDR5 5200MHz',
                'storage': '2TB NVMe SSD + 4TB HDD',
                'gpu': 'NVIDIA RTX 3080 Ti 12GB',
                'psu': '1000W 80+ Platinum',
                'cooling': 'NZXT Kraken Z73 360mm AIO',
                'case': 'Lian Li O11 Dynamic',
                'os': 'Windows 11 Pro'
            }
        },
        {
            'name': 'SS Creative Studio - AMD Edition',
            'description': 'Powerful workstation for content creators with AMD Ryzen 9',
            'price': 179999.99,
            'category': 'prebuilt',
            'image_url': 'https://via.placeholder.com/300x300.png?text=Creative+Studio+AMD',
            'stock': 5,
            'specs': {
                'processor': 'AMD Ryzen 9 5900X',
                'processor_family': 'Ryzen 9',
                'motherboard': 'ASUS ROG Crosshair VIII Hero',
                'ram': '64GB DDR4 3600MHz',
                'storage': '1TB NVMe SSD + 2TB SATA SSD',
                'gpu': 'NVIDIA RTX 3070 8GB',
                'psu': '850W 80+ Gold',
                'cooling': 'Corsair H150i RGB PRO XT 360mm AIO',
                'case': 'Fractal Design Meshify 2',
                'os': 'Windows 11 Pro'
            }
        }
    ]
    
    for pc_data in prebuilt_pcs:
        existing = Product.query.filter_by(name=pc_data['name']).first()
        if not existing:
            pc = Product(
                name=pc_data['name'],
                description=pc_data['description'],
                price=pc_data['price'],
                category=pc_data['category'],
                image_url=pc_data['image_url'],
                stock=pc_data['stock'],
                specs=pc_data['specs']
            )
            db.session.add(pc)
    
    db.session.commit()
    
    flash('Sample data has been added to the database.', 'success')
    return redirect(url_for('admin_panel'))
