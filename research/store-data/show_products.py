import sqlite3
import csv
from dataclasses import dataclass
from store_to_db import Product

# Step 2: Connect to SQLite Database (or create it if it doesn't exist)
connection = sqlite3.connect('products.db')
cursor = connection.cursor()

# Step 5: Retrieve data from the database and output as Product instances
cursor.execute("SELECT id, name, category, sub_category, price, vat_rate,organization_id, org_unit_id, created_date FROM products")
rows = cursor.fetchall()

# Convert each row to a Product instance and print it

# for row in rows:
    # print(row, '\n\n')

# print(rows)
retrieved_products = [Product(*row) for row in rows]

for product in retrieved_products:
    print(product)

# # Close the database connection
connection.close()