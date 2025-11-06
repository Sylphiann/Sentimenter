from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('query', views.search_result, name='query'),
]