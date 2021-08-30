from django.urls import path
from .views import user_favorite_list, null_orders

urlpatterns = [
    path('reports/userfavorites', user_favorite_list),
    path('reports/nullorders', null_orders),
]