"""roots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views.view_router import *
from .views.login_view import LoginView

urlpatterns = [
    # Authentication URLs
    # path('api-token-auth/', views.CustomAuthToken.as_view()),
    # path('passwordReset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    # User URLs
    path('users/', user_route),
    path('createUser/', create_user_route),
    path('login/', LoginView.as_view()),

    # Order URLs
    path('order/', order_route),

    # Markets URLs

    # Customer Urls
    path('marketFarmSearch/', market_farm_search_route),

    # Farmer routes
    path('marketInfo/', farmer_market_info_route),
    path('farmVegetables/', farmer_farm_vegetable_route),
    path('farms/', farmer_farm_route),
    path('markets/', farmer_market_route),
]
