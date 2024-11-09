from django.http import JsonResponse
from .models import Product

def get_unique_categories(request=None):
    # Query all products and extract categories
    categories = Product.objects.values_list('category', flat=True).distinct()
    subcategories = Product.objects.values_list('sub_category', flat=True).distinct()

    # Convert the queryset to a Python set to ensure uniqueness
    category_set = set(categories)
    subcategory_set = set(subcategories)

    # Prepare the response data as a dictionary
    data = {
        'categories': list(category_set),  # Convert set to list for JSON serialization
        'subcategories': list(subcategory_set)  # Convert set to list for JSON serialization
    }

    return JsonResponse(data)