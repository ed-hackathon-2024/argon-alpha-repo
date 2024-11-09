# views.py
import csv
from django.http import JsonResponse
from django.conf import settings
from .models import Product
from rest_framework.decorators import api_view

import os

@api_view(['GET'])
def load_products_from_csv(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'new-products.csv')  # path to your CSV file

    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        products = []

        for row in csv_reader:
            price = float(row["price"]) if row["price"].replace('.', '', 1).isdigit() else 0.0
            vat_rate = float(row["vat_rate"]) if row["vat_rate"].replace('.', '', 1).isdigit() else 0.0
            val = row.get("id", "")
            try:
                product = Product(
                    id = int(row.get("id", "")),
                    name=row.get("name", ""),
                    category=row.get("category", ""),
                    sub_category=row.get("sub_category", ""),
                    price=price,
                    vat_rate=vat_rate,
                    organization_id=row.get("organization_id", ""),
                    org_unit_id=row.get("org_unit_id", ""),
                    created_date=row.get("created_date", "")
                )
            except:
                break

            products.append(product)

        # Bulk create all products at once for efficiency
        Product.objects.bulk_create(products)

    return JsonResponse({'status': 'success', 'message': 'Products loaded successfully'})