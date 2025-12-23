"""
Enhanced Database Initialization Script for InsightGen
Creates comprehensive sample data for testing dashboard generation
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.models import Base, Product, Customer, Order
from app.db.session import engine, SessionLocal
from app.config import settings

# Sample data
CATEGORIES = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Toys', 'Food & Beverage']
REGIONS = ['North', 'South', 'East', 'West', 'Central']
CITIES = {
    'North': ['New York', 'Boston', 'Chicago', 'Detroit'],
    'South': ['Miami', 'Atlanta', 'Houston', 'Dallas'],
    'East': ['Philadelphia', 'Baltimore', 'Washington DC'],
    'West': ['Los Angeles', 'San Francisco', 'Seattle', 'Portland'],
    'Central': ['Denver', 'Kansas City', 'St. Louis', 'Minneapolis']
}

PRODUCT_NAMES = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smart Watch', 'Camera', 'Speaker', 'Monitor'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Dress', 'Shoes', 'Hat', 'Scarf', 'Sweater'],
    'Home & Garden': ['Sofa', 'Table', 'Chair', 'Lamp', 'Rug', 'Plant', 'Vase', 'Mirror'],
    'Sports': ['Basketball', 'Soccer Ball', 'Tennis Racket', 'Yoga Mat', 'Dumbbell', 'Bicycle', 'Skateboard'],
    'Books': ['Fiction Novel', 'Cookbook', 'Biography', 'Self-Help', 'Science', 'History', 'Poetry'],
    'Toys': ['Action Figure', 'Doll', 'Board Game', 'Puzzle', 'LEGO Set', 'RC Car', 'Stuffed Animal'],
    'Food & Beverage': ['Coffee', 'Tea', 'Chocolate', 'Cookies', 'Juice', 'Snacks', 'Pasta']
}

FIRST_NAMES = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 'James', 'Mary',
               'William', 'Patricia', 'Richard', 'Jennifer', 'Thomas', 'Linda', 'Charles', 'Barbara',
               'Daniel', 'Susan', 'Matthew', 'Jessica', 'Anthony', 'Karen', 'Mark', 'Nancy']

LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez',
              'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor',
              'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris', 'Clark']


def create_products(session):
    """Create diverse product catalog"""
    print("Creating products...")
    products = []
    product_id = 1
    
    for category in CATEGORIES:
        product_names = PRODUCT_NAMES.get(category, ['Product'])
        for product_name in product_names:
            # Create 2-3 variants per product
            for variant in range(random.randint(2, 3)):
                price = round(random.uniform(10, 500), 2)
                
                # Add variant suffix
                if variant > 0:
                    full_name = f"{product_name} - {['Standard', 'Premium', 'Deluxe'][variant]}"
                else:
                    full_name = product_name
                
                product = Product(
                    product_id=product_id,
                    product_name=full_name,
                    category=category,
                    price=price
                )
                products.append(product)
                product_id += 1
    
    session.bulk_save_objects(products)
    session.commit()
    print(f"✓ Created {len(products)} products across {len(CATEGORIES)} categories")
    return products


def create_customers(session):
    """Create diverse customer base"""
    print("Creating customers...")
    customers = []
    customer_id = 1
    
    for _ in range(100):  # 100 customers
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        region = random.choice(REGIONS)
        
        customer = Customer(
            customer_id=customer_id,
            customer_name=f"{first_name} {last_name}",
            region=region
        )
        customers.append(customer)
        customer_id += 1
    
    session.bulk_save_objects(customers)
    session.commit()
    print(f"✓ Created {len(customers)} customers across {len(REGIONS)} regions")
    return customers


def create_orders(session, products, customers):
    """Create realistic order history"""
    print("Creating orders...")
    orders = []
    order_id = 1
    
    # Generate orders over the past 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Create 2000 orders
    for _ in range(2000):
        # Random date within the past year
        days_ago = random.randint(0, 365)
        order_date = end_date - timedelta(days=days_ago)
        
        # Pick random customer and product
        customer = random.choice(customers)
        product = random.choice(products)
        
        # Quantity varies by product category
        if product.category in ['Electronics', 'Home & Garden']:
            quantity = random.randint(1, 3)
        elif product.category in ['Clothing', 'Sports']:
            quantity = random.randint(1, 5)
        else:
            quantity = random.randint(1, 10)
        
        # Calculate revenue with occasional discounts
        discount = random.choice([1.0, 1.0, 1.0, 0.9, 0.85, 0.8])  # 70% full price
        revenue = round(product.price * quantity * discount, 2)
        
        order = Order(
            order_id=order_id,
            customer_id=customer.customer_id,
            product_id=product.product_id,
            order_date=order_date,
            quantity=quantity,
            revenue=revenue
        )
        orders.append(order)
        order_id += 1
    
    session.bulk_save_objects(orders)
    session.commit()
    print(f"✓ Created {len(orders)} orders over 12 months")
    return orders


def print_summary(session):
    """Print database summary"""
    print("\n" + "=" * 60)
    print("DATABASE SUMMARY")
    print("=" * 60)
    
    # Products by category
    from sqlalchemy import func
    product_counts = session.query(
        Product.category,
        func.count(Product.product_id).label('count')
    ).group_by(Product.category).all()
    
    print("\nProducts by Category:")
    for category, count in product_counts:
        print(f"  {category}: {count} products")
    
    # Customers by region
    customer_counts = session.query(
        Customer.region,
        func.count(Customer.customer_id).label('count')
    ).group_by(Customer.region).all()
    
    print("\nCustomers by Region:")
    for region, count in customer_counts:
        print(f"  {region}: {count} customers")
    
    # Order statistics
    total_orders = session.query(func.count(Order.order_id)).scalar()
    total_revenue = session.query(func.sum(Order.revenue)).scalar()
    avg_order_value = session.query(func.avg(Order.revenue)).scalar()
    
    print(f"\nOrder Statistics:")
    print(f"  Total Orders: {total_orders:,}")
    print(f"  Total Revenue: ${total_revenue:,.2f}")
    print(f"  Average Order Value: ${avg_order_value:.2f}")
    
    # Date range
    min_date = session.query(func.min(Order.order_date)).scalar()
    max_date = session.query(func.max(Order.order_date)).scalar()
    print(f"  Date Range: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}")
    
    print("\n" + "=" * 60)


def main():
    print("=" * 60)
    print("InsightGen Enhanced Database Setup")
    print("=" * 60)
    
    # Create tables
    print("\nCreating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")
    
    # Create session
    session = SessionLocal()
    
    try:
        # Populate data
        print("\nPopulating sample data...")
        products = create_products(session)
        customers = create_customers(session)
        orders = create_orders(session, products, customers)
        
        print("\n✓ Sample data populated successfully!")
        
        # Print summary
        print_summary(session)
        
        print("\n" + "=" * 60)
        print("Database setup complete!")
        print("=" * 60)
        print("\nSample queries you can try:")
        print("  - 'Show me total sales by category'")
        print("  - 'Top 10 customers by revenue'")
        print("  - 'Monthly sales trends for Electronics'")
        print("  - 'Which region has the highest sales?'")
        print("  - 'Compare sales across all categories'")
        print("  - 'Show sales by city in the North region'")
        print("  - 'What are the best selling products?'")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
