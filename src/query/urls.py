from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('query', views.search_result, name='query'),
    path('set-sentiment', views.set_sentiment, name='set-sentiment'),
    path('remove-sentiment', views.remove_sentiment, name='remove-sentiment'),
]