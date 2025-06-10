from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os
import uuid
import json
import logging
from sqlalchemy import or_

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
    static_folder='frontend/static',
    template_folder='frontend/templates'
)
# Configure CORS to allow requests from frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a secure secret key

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Product Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='category', lazy=True)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Chat Session model
class ChatSession(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('ChatMessage', backref='session', lazy=True)

# Chat Message model
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('chat_session.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_bot = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables and add sample data
def init_db():
    with app.app_context():
        logger.info("Creating database tables...")
        db.create_all()
        
        # Check if categories already exist
        if Category.query.count() == 0:
            logger.info("Adding sample categories...")
            categories = [
                Category(name='Electronics', description='Electronic devices and gadgets'),
                Category(name='Books', description='Books and publications'),
                Category(name='Clothing', description='Fashion and apparel'),
                Category(name='Home & Kitchen', description='Home appliances and kitchenware')
            ]
            db.session.add_all(categories)
            db.session.commit()
            logger.info("Categories added successfully")

        # Check if products already exist
        if Product.query.count() == 0:
            logger.info("Adding sample products...")
            products = [
                Product(
                    name='Smartphone X',
                    description='Latest smartphone with advanced features',
                    price=699.99,
                    stock=50,
                    category_id=1,
                    image_url='/static/images/smartphone.jpg'
                ),
                Product(
                    name='Laptop Pro',
                    description='High-performance laptop for professionals',
                    price=1299.99,
                    stock=30,
                    category_id=1,
                    image_url='/static/images/laptop.jpg'
                ),
                Product(
                    name='Design Patterns Book',
                    description='Essential guide to software design patterns',
                    price=39.99,
                    stock=100,
                    category_id=2,
                    image_url='/static/images/book.jpg'
                ),
                Product(
                    name='Classic T-Shirt',
                    description='Comfortable cotton t-shirt',
                    price=19.99,
                    stock=200,
                    category_id=3,
                    image_url='/static/images/tshirt.jpg'
                ),
                Product(
                    name='Wireless Earbuds',
                    description='High-quality wireless earbuds with noise cancellation',
                    price=149.99,
                    stock=75,
                    category_id=1,
                    image_url='/static/images/earbuds.jpg'
                ),
                Product(
                    name='Smart Watch',
                    description='Feature-rich smartwatch with health monitoring',
                    price=199.99,
                    stock=40,
                    category_id=1,
                    image_url='/static/images/smartwatch.jpg'
                ),
                Product(
                    name='Coffee Maker',
                    description='Automatic coffee maker with timer',
                    price=79.99,
                    stock=60,
                    category_id=4,
                    image_url='/static/images/coffeemaker.jpg'
                ),
                Product(
                    name='Design Patterns Book',
                    description='Comprehensive guide to software architecture',
                    price=49.99,
                    stock=80,
                    category_id=2,
                    image_url='/static/images/designbook.jpg'
                ),
                Product(
                    name='Denim Jacket',
                    description='Classic denim jacket for all seasons',
                    price=89.99,
                    stock=45,
                    category_id=3,
                    image_url='/static/images/jacket.jpg'
                )
            ]
            db.session.add_all(products)
            db.session.commit()
            logger.info("Products added successfully")

# Initialize database with sample data
init_db()

# Product routes
@app.route('/api/products', methods=['GET'])
def get_products():
    category_id = request.args.get('category_id', type=int)
    search_query = request.args.get('search', '')
    
    query = Product.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))
    
    products = query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'stock': p.stock,
        'category_id': p.category_id,
        'image_url': p.image_url
    } for p in products])

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description
    } for c in categories])

# Enhanced chat message handling
def process_chat_message(message):
    """Process incoming chat messages and generate appropriate responses"""
    message = message.lower().strip()
    
    # Handle greetings
    greetings = ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
    if message in greetings:
        return "Hello! I'm your shopping assistant. How can I help you today? You can ask me about products, search for specific items, or browse categories."
    
    # Handle help requests
    if 'help' in message or 'what can you do' in message:
        return "I can help you with:\n1. Searching for products\n2. Browsing categories\n3. Checking prices and stock\n4. Finding specific items\nJust let me know what you're looking for!"
    
    # Handle product search - including single word searches
    search_terms = message
    if 'search' in message or 'find' in message or 'looking for' in message:
        search_terms = message.replace('search', '').replace('find', '').replace('looking for', '').strip()
    
    # Search for products
    products = Product.query.filter(
        or_(
            Product.name.ilike(f'%{search_terms}%'),
            Product.description.ilike(f'%{search_terms}%')
        )
    ).all()
    
    if products:
        response = "Here are the products I found:\n\n"
        for product in products:
            response += f"Product: {product.name}\n"
            response += f"Price: ${product.price}\n"
            response += f"Stock: {product.stock} units available\n"
            response += f"Description: {product.description}\n"
            response += "-------------------\n"
        return response
    
    # Handle category browsing
    if 'category' in message or 'categories' in message or 'browse' in message:
        categories = Category.query.all()
        response = "Here are our available categories:\n\n"
        for category in categories:
            response += f"- {category.name}: {category.description}\n"
        response += "\nYou can ask me about products in any of these categories."
        return response
    
    # Handle price inquiries
    if 'price' in message or 'cost' in message or 'how much' in message:
        # Extract product name
        product_name = message.replace('price', '').replace('cost', '').replace('how much', '').strip()
        if product_name:
            product = Product.query.filter(Product.name.ilike(f'%{product_name}%')).first()
            if product:
                return f"The {product.name} costs ${product.price}. We have {product.stock} units in stock."
            else:
                return f"I couldn't find a product named '{product_name}'. Could you please specify the product name?"
    
    # Handle stock inquiries
    if 'stock' in message or 'available' in message or 'in stock' in message:
        # Extract product name
        product_name = message.replace('stock', '').replace('available', '').replace('in stock', '').strip()
        if product_name:
            product = Product.query.filter(Product.name.ilike(f'%{product_name}%')).first()
            if product:
                return f"We have {product.stock} units of {product.name} in stock."
            else:
                return f"I couldn't find a product named '{product_name}'. Could you please specify the product name?"
    
    # If no matches found, show available categories and some products
    categories = Category.query.all()
    response = "I couldn't find any products matching your search. Here are our available categories:\n\n"
    for category in categories:
        response += f"- {category.name}: {category.description}\n"
    
    response += "\nYou can try:\n1. Searching with different terms\n2. Browsing by category\n3. Asking about specific products"
    return response

# Update the chat message endpoint to use the enhanced processing
@app.route('/api/chat/message', methods=['POST'])
def send_chat_message():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No token provided'}), 401
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        data = request.get_json()
        
        session = ChatSession.query.get(data['session_id'])
        if not session or session.user_id != user_id:
            return jsonify({'error': 'Invalid session'}), 400
        
        # Save user message
        user_message = ChatMessage(
            session_id=session.id,
            content=data['content'],
            is_bot=False
        )
        db.session.add(user_message)
        
        # Process message and generate bot response
        bot_response = process_chat_message(data['content'])
        bot_message = ChatMessage(
            session_id=session.id,
            content=bot_response,
            is_bot=True
        )
        db.session.add(bot_message)
        db.session.commit()
        
        return jsonify({'bot_response': bot_response})
    except:
        return jsonify({'error': 'Invalid token'}), 401

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, app.config['SECRET_KEY'])
        
        return jsonify({
            'access_token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No token provided'}), 401
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(payload['user_id'])
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    except:
        return jsonify({'error': 'Invalid token'}), 401

# Chat routes
@app.route('/api/chat/session', methods=['POST'])
def create_chat_session():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No token provided'}), 401
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        
        session = ChatSession(id=str(uuid.uuid4()), user_id=user_id)
        db.session.add(session)
        db.session.commit()
        
        return jsonify({'session_id': session.id})
    except:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/api/chat/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No token provided'}), 401
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        
        session = ChatSession.query.get(session_id)
        if not session or session.user_id != user_id:
            return jsonify({'error': 'Invalid session'}), 400
        
        messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at).all()
        return jsonify({
            'messages': [{
                'content': msg.content,
                'is_bot': msg.is_bot,
                'created_at': msg.created_at.isoformat()
            } for msg in messages]
        })
    except:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/api/chat/reset/<session_id>', methods=['POST'])
def reset_chat(session_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No token provided'}), 401
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        
        session = ChatSession.query.get(session_id)
        if not session or session.user_id != user_id:
            return jsonify({'error': 'Invalid session'}), 400
        
        # Delete all messages in the session
        ChatMessage.query.filter_by(session_id=session_id).delete()
        db.session.commit()
        
        return jsonify({'new_session_id': session_id})
    except:
        return jsonify({'error': 'Invalid token'}), 401

# Add a debug route to check database content
@app.route('/api/debug/products', methods=['GET'])
def debug_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'stock': p.stock,
        'category_id': p.category_id
    } for p in products])

# Add this route to serve static images
@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/static/images/placeholder.jpg')
def serve_placeholder():
    return send_from_directory('static/images', 'placeholder.jpg')

# Serve the main page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 