from django.urls import path
from .getSessionData import get_session_data
from .getProducts import get_products
from .initData import load_products_from_csv
from .getCategories import get_unique_categories
from .views import generate_category_content, generate_notes_view , generate_category_activity
from .getCategoriesForGraph import get_categories_for_graph
from .get_monthly_transactions import get_transactions_for_month

urlpatterns = [
    path('get_categories_activity/', generate_category_activity, name='generate_categories_activity'),
    path('get_category_contente/', generate_category_content, name='generate_category_content' ),
    path('get_session_data/', get_session_data, name='getSessionData' ),
    path('get_notes_content/', generate_notes_view, name='generate_category_content' ),
    path('get-products/', get_products, name='get_products' ),
    path('init_data/', load_products_from_csv, name='init_data' ),
    path('getCategories/', get_unique_categories, name='get_unique_categories' ),
    path('getCategoriesForGraph/', get_categories_for_graph, name='get_categories_for_graph' ),
    path('get_transactions_for_month/', get_transactions_for_month, name='get_transactions_for_month' ),

    
]
