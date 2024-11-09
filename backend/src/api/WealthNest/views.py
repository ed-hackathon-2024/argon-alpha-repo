from sqlite3 import connect

import json
from loguru import logger
from django.views.decorators.csrf import csrf_exempt
from .ai.exceptions import ResponseNotGeneratedError
from .ai.manager import Manager
from rest_framework.response import Response
from rest_framework.views import APIView
from os import getenv
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from .ai.chat_management import ChatAssistant



from .ai.saving_category_content_generator import generate_saving_category_content, StatisticalInformation, \
    CategoryInformation
from .ai.user_notes_content_generator import generate_notes_content, UserInformation
from .getCategories import get_unique_categories


def get_manager():
    """Helper function to instantiate Manager with model and API key."""
    model = "gpt-4o-mini"
    api_key = getenv("api_key")
    if not api_key:
        raise ValueError("API key is missing. Ensure 'api_key' is set in the environment.")
    return Manager(model, api_key)



@csrf_exempt
def generate_category_activity(request):
    categories = get_unique_categories()
    return categories



@csrf_exempt
async def generate_category_content(request):
    user_goal = request.POST.get("user_goal")
    statistical_name = request.POST.get("category_name")
    category_information = CategoryInformation(
        name = "John smith",
        monthly_expenses = 300,
        currency = "euro",
        transactions_amount =  5
    )
    statistical_info =  StatisticalInformation(
        common_transaction_name = statistical_name
    )
    try:
        content = await generate_saving_category_content(get_manager(), category_information ,statistical_info, user_goal)
        return JsonResponse(content)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
async def generate_notes_view(request):

    data = json.loads(request.body)

    user_info = UserInformation(
        name="Johny Smith",
        age="24",
        gender="Male",
        goal=data.get("goal")
    )

    content = await generate_notes_content(get_manager(), user_info)
    return JsonResponse(content)

