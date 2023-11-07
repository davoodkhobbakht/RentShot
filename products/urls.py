"""
URL configuration for RentShot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import *

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/reserve/', reserve_product, name='reserve_product'),
    path('product/<int:product_id>/availability/', product_availability, name='product_availability'),

    # URL pattern for initiating the payment
    path('initiate-payment/<int:reservation_id>/', initiate_payment, name='initiate_payment'),

    # URL pattern for verifying the payment (callback)
    path('verify-payment/', verify_payment, name='verify_payment'),
]

