from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='admin-sentence', permanent=True)),
    path('sentence', RedirectView.as_view(pattern_name='admin-sentence', permanent=True)),
    path('sentence/', views.admin_tools_view, name='admin-sentence'),
]