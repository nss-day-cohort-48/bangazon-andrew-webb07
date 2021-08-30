from django.urls import path
from .views import user_favorite_list

urlpatterns = [
    path('reports/userfavorites', user_favorite_list),
]