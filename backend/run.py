from app import create_app
from app.utils.seed_data import seed_products

app = create_app()

if __name__ == '__main__':
    # Seed the database with mock data if it's empty
    with app.app_context():
        from app.models.product import Product
        if Product.query.count() == 0:
            seed_products()
    
    app.run(debug=True) 