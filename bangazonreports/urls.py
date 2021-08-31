from django.urls import path
from .views import user_favorite_list, null_orders, completed_orders, inexpensive_products, expensive_products

urlpatterns = [
    path('reports/userfavorites', user_favorite_list),
    path('reports/nullorders', null_orders),
    path('reports/completedorders', completed_orders),
    path('reports/inexpensiveproducts', inexpensive_products),
    path('reports/expensiveproducts', expensive_products)
]