from django.contrib import admin
from .views import *
from django.urls import path

app_name = 'coupon'
urlpatterns = [
    path('add/', add_coupon, name='add'),
]
