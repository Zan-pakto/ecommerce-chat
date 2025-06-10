from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models.product import Product
from .. import db
from sqlalchemy import or_

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'name')
    sort_order = request.args.get('sort_order', 'asc')
    
    # Base query
    query = Product.query
    
    # Apply filters
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%'),
                Product.brand.ilike(f'%{search}%')
            )
        )
    
    # Apply sorting
    if sort_by in ['name', 'price', 'rating']:
        sort_column = getattr(Product, sort_by)
        if sort_order == 'desc':
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    
    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'products': [product.to_dict() for product in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(product.to_dict()), 200

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Product.category).distinct().all()
    return jsonify([category[0] for category in categories if category[0]]), 200

@products_bp.route('/featured', methods=['GET'])
def get_featured_products():
    featured = Product.query.filter_by(is_featured=True).limit(6).all()
    return jsonify([product.to_dict() for product in featured]), 200

@products_bp.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    products = Product.query.filter(
        or_(
            Product.name.ilike(f'%{query}%'),
            Product.description.ilike(f'%{query}%'),
            Product.brand.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    return jsonify([product.to_dict() for product in products]), 200 