from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .apps import WealthNestConfig 

@api_view(['GET'])
def get_products(request=None):

    # data = WealthNestConfig.get_data()

    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)