import sqlite3
import csv
from dataclasses import dataclass

# Step 1: Define the Product dataclass
@dataclass
class Product:
    id: str
    name: str
    category: str
    sub_category: str
    price: float
    vat_rate: float
    organization_id: str
    org_unit_id: str
    created_date: str

# Step 2: Connect to SQLite Database (or create it if it doesn't exist)
connection = sqlite3.connect('products.db')
cursor = connection.cursor()

# Step 3: Create the Product table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        category TEXT,
        sub_category TEXT,
        price REAL,
        vat_rate REAL,
        organization_id TEXT,
        org_unit_id TEXT,
        created_date TEXT
    )
''')
print("Table created successfully.")

# Step 4: Read data from CSV file and insert it into the database
with open('new-products.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    
    products = []  # This will hold Product instances
    
    for row in csv_reader:

        price = float(row["price"]) if row["price"].replace('.', '', 1).isdigit() else 0.0
        vat_rate = float(row["vat_rate"]) if row["vat_rate"].replace('.', '', 1).isdigit() else 0.0


        # Create a Product instance
        product = Product(
            id=row.get("id", ""),
            name=row.get("name", ""),
            category=row.get("category", ""),
            sub_category=row.get("sub_category", ""),
            price = price,
            vat_rate=vat_rate,
            organization_id=row.get("organization_id", ""),
            org_unit_id= row.get("org_unit_id", ""),
            created_date=row.get("created_date", "")
        )

        
        print(f"Try insert product: {product}")
        try:
            cursor.execute('''
                    INSERT INTO products (id, name, category, sub_category, price, vat_rate, organization_id, org_unit_id, created_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    product.id, product.name, product.category, product.sub_category,
                    product.price, product.vat_rate, product.organization_id,
                    product.org_unit_id, product.created_date
                ))
        except sqlite3.IntegrityError as e:
            print(f"Failed to insert product {product}: {e}")
        
        

# Insert all data into the database
# cursor.executemany('''
#     INSERT INTO products (id, name, category, sub_category, organization_id, org_unit_id, created_date)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# ''', products)
# print("Data inserted successfully.")

# Commit the transaction and close the connection
connection.commit()
connection.close()


