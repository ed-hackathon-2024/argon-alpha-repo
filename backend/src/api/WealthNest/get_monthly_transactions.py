from django.http import JsonResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from .models import Product
from datetime import datetime

def get_transactions_for_month(request, month=None):
    pass
    # if month is None and request is not None:
    #     month = request.GET.get('month')


    # try:
    #     # Parse the month parameter (expected format: 'YYYY-MM')
    #     target_month = datetime.strptime(month, '%Y-%m')
    # except ValueError:
    #     return JsonResponse({'error': 'Invalid month format. Use YYYY-MM.'}, status=400)

    # # Aggregate data for the specified month
    # monthly_data = Product.objects.annotate(month=TruncMonth('created_date')).filter(
    #     month=target_month
    # ).aggregate(
    #     transaction_count=Count('id'),
    #     total_price=Sum('price')
    # )

    # # Check if there are any transactions for the month
    # if monthly_data['transaction_count'] == 0:
    #     return JsonResponse({'message': 'No transactions found for this month.'})

    # # Return the transaction count and total price
    # data = {
    #     'month': month,
    #     'transaction_count': monthly_data['transaction_count'],
    #     'total_price': monthly_data['total_price'] or 0  # Handle None if no transactions
    # }

    # return JsonResponse(data)
