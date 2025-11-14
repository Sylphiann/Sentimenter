from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='admin-sentence', permanent=True)),
    path('sentence', RedirectView.as_view(pattern_name='admin-sentence', permanent=True)),
    path('sentence/', views.admin_sentence_view, name='admin-sentence'),

    path('sentiment', RedirectView.as_view(pattern_name='admin-sentiment', permanent=True)),
    path('sentiment/', views.admin_sentiment_view, name='admin-sentiment'),
]