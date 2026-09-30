import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)

NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 200
NUM_ORDERS = 20000

OUTPUT_DIR = Path(__file__).parent


# ============================================================
# REFERENCE DATA
# ============================================================

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Rahul",
    "Rohan", "Karan", "Kabir", "Aryan", "Vikram",
    "Ananya", "Aisha", "Diya", "Isha", "Meera",
    "Priya", "Riya", "Sneha", "Kavya", "Nisha"
]

LAST_NAMES = [
    "Sharma", "Gupta", "Patel", "Mehta", "Verma",
    "Kapoor", "Malhotra", "Singh", "Shah", "Joshi",
    "Reddy", "Iyer", "Nair", "Desai", "Bhat"
]

CITIES = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Surat"
]

SEGMENTS = [
    "Premium",
    "Regular",
    "Budget"
]

CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Beauty",
    "Sports",
    "Books"
]

PAYMENT_METHODS = [
    "Credit Card",
    "Debit Card",
    "UPI",
    "Net Banking",
    "Cash on Delivery"
]

ORDER_STATUSES = [
    "Completed",
    "Completed",
    "Completed",
    "Completed",
    "Cancelled",
    "Returned"
]


# ============================================================
# CUSTOMERS
# ============================================================

def generate_customers():
    customers = []

    start_date = datetime(2023, 1, 1)

    for customer_id in range(1, NUM_CUSTOMERS + 1):

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        signup_date = start_date + timedelta(
            days=random.randint(0, 900)
        )

        customers.append({
            "customer_id": customer_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}"
                    f"{customer_id}@example.com",
            "city": random.choice(CITIES),
            "segment": random.choices(
                SEGMENTS,
                weights=[15, 55, 30],
                k=1
            )[0],
            "signup_date": signup_date.date()
        })

    return pd.DataFrame(customers)


# ============================================================
# PRODUCTS
# ============================================================

def generate_products():
    products = []

    product_names = {
        "Electronics": [
            "Wireless Headphones",
            "Smartphone",
            "Laptop",
            "Smart Watch",
            "Bluetooth Speaker",
            "Tablet"
        ],
        "Clothing": [
            "T-Shirt",
            "Jeans",
            "Jacket",
            "Sneakers",
            "Hoodie",
            "Formal Shirt"
        ],
        "Home & Kitchen": [
            "Coffee Maker",
            "Air Fryer",
            "Mixer Grinder",
            "Cookware Set",
            "Bedsheet",
            "Vacuum Cleaner"
        ],
        "Beauty": [
            "Face Serum",
            "Moisturizer",
            "Perfume",
            "Face Wash",
            "Hair Dryer",
            "Makeup Kit"
        ],
        "Sports": [
            "Running Shoes",
            "Yoga Mat",
            "Dumbbells",
            "Cricket Bat",
            "Football",
            "Tennis Racket"
        ],
        "Books": [
            "Python Programming",
            "Data Science Handbook",
            "Atomic Habits",
            "Machine Learning Guide",
            "Business Analytics",
            "AI Fundamentals"
        ]
    }

    for product_id in range(1, NUM_PRODUCTS + 1):

        category = random.choice(CATEGORIES)
        name = random.choice(product_names[category])

        cost = round(random.uniform(200, 15000), 2)

        # Selling price is always above cost
        price = round(
            cost * random.uniform(1.15, 2.2),
            2
        )

        products.append({
            "product_id": product_id,
            "product_name": f"{name} {product_id}",
            "category": category,
            "cost": cost,
            "price": price
        })

    return pd.DataFrame(products)


# ============================================================
# ORDERS
# ============================================================

def generate_orders(customers, products):
    orders = []
    order_items = []

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)

    for order_id in range(1, NUM_ORDERS + 1):

        customer = customers.sample(1).iloc[0]
        product = products.sample(1).iloc[0]

        order_date = start_date + timedelta(
            days=random.randint(
                0,
                (end_date - start_date).days
            )
        )

        quantity = random.randint(1, 5)

        status = random.choice(ORDER_STATUSES)

        discount = round(
            random.uniform(0, 0.25),
            2
        )

        unit_price = product["price"]

        total_amount = round(
            quantity * unit_price * (1 - discount),
            2
        )

        orders.append({
            "order_id": order_id,
            "customer_id": customer["customer_id"],
            "order_date": order_date.date(),
            "status": status,
            "payment_method": random.choice(PAYMENT_METHODS),
            "discount": discount,
            "total_amount": total_amount
        })

        order_items.append({
            "order_item_id": order_id,
            "order_id": order_id,
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": unit_price
        })

    return (
        pd.DataFrame(orders),
        pd.DataFrame(order_items)
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("Generating customers...")
    customers = generate_customers()

    print("Generating products...")
    products = generate_products()

    print("Generating orders...")
    orders, order_items = generate_orders(
        customers,
        products
    )

    customers.to_csv(
        OUTPUT_DIR / "customers.csv",
        index=False
    )

    products.to_csv(
        OUTPUT_DIR / "products.csv",
        index=False
    )

    orders.to_csv(
        OUTPUT_DIR / "orders.csv",
        index=False
    )

    order_items.to_csv(
        OUTPUT_DIR / "order_items.csv",
        index=False
    )

    print("\nData generation completed!")
    print("--------------------------------")
    print(f"Customers:   {len(customers):,}")
    print(f"Products:    {len(products):,}")
    print(f"Orders:      {len(orders):,}")
    print(f"Order Items: {len(order_items):,}")
    print("--------------------------------")


if __name__ == "__main__":
    main()
    