from django.contrib import admin
from .views import *
from django.urls import path

app_name = 'cart'
urlpatterns = [
    path('', detail, name='detail'),
    path('add/<int:product_id>/', add, name="product_add"),
    path('remove/<int:product_id>/', remove, name="product_remove"),
]
