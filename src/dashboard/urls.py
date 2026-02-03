from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='admin-sentence', permanent=True)),
    path('sentence', RedirectView.as_view(pattern_name='admin-sentence', permanent=True)),
    path('sentence/', views.admin_sentence_view, name='admin-sentence'),

    path('setup/', views.DashboardRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(
            template_name='dashboard/login.html',
            next_page='admin-sentence'
        ), 
        name='login'
    ),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('sentiment', RedirectView.as_view(pattern_name='admin-sentiment', permanent=True)),
    path('sentiment/', views.admin_sentiment_view, name='admin-sentiment'),
]