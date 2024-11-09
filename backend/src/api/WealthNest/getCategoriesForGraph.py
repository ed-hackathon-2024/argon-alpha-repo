from django.http import JsonResponse
from django.db.models import Count, Sum
from .models import Product

def get_categories_for_graph(request=None):
    # Query all products and extract categories
    categories_data = Product.objects.values('category').annotate(
        item_count=Count('id'),           # Count of items in each category
        total_price=Sum('price')           # Sum of prices in each category
    )

    # Prepare the response data as a list of dictionaries
    data = [
        {
            'category': entry['category'],
            'item_count': entry['item_count'],
            'total_price': entry['total_price']
        }
        for entry in categories_data
    ]

    return JsonResponse({'categories': data})