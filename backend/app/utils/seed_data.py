from ..models.product import Product
from .. import db
import random
from datetime import datetime

def seed_products():
    # Sample product categories
    categories = ['Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports']
    brands = ['TechPro', 'BookWorld', 'StyleHub', 'HomeEssentials', 'SportLife']
    
    # Sample product names and descriptions
    product_templates = [
        {
            'name': '{} {}',
            'description': 'High-quality {} with advanced features and modern design.',
            'price_range': (19.99, 999.99),
            'stock_range': (0, 100)
        },
        {
            'name': 'Premium {} {}',
            'description': 'Professional-grade {} built to last with exceptional performance.',
            'price_range': (49.99, 1499.99),
            'stock_range': (0, 50)
        },
        {
            'name': 'Deluxe {} {}',
            'description': 'Luxury {} offering superior quality and unmatched comfort.',
            'price_range': (99.99, 1999.99),
            'stock_range': (0, 25)
        }
    ]
    
    # Product types for each category
    category_products = {
        'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smartwatch'],
        'Books': ['Novel', 'Textbook', 'Cookbook', 'Biography', 'Self-Help'],
        'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes'],
        'Home & Kitchen': ['Blender', 'Coffee Maker', 'Toaster', 'Cookware Set', 'Cutlery'],
        'Sports': ['Basketball', 'Tennis Racket', 'Yoga Mat', 'Running Shoes', 'Dumbbells']
    }
    
    # Generate and add products
    for category in categories:
        for product_type in category_products[category]:
            for template in product_templates:
                # Create multiple variations of each product
                for i in range(3):
                    product = Product(
                        name=template['name'].format(product_type, i+1),
                        description=template['description'].format(product_type),
                        price=round(random.uniform(*template['price_range']), 2),
                        stock=random.randint(*template['stock_range']),
                        category=category,
                        brand=random.choice(brands),
                        rating=round(random.uniform(1.0, 5.0), 1),
                        review_count=random.randint(0, 1000),
                        is_featured=random.random() < 0.2,  # 20% chance of being featured
                        image_url=f'https://example.com/images/{category.lower()}/{product_type.lower()}_{i+1}.jpg'
                    )
                    db.session.add(product)
    
    # Commit all products to the database
    db.session.commit()

if __name__ == '__main__':
    seed_products() 