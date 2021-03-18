from django.contrib import admin
from .views import *
from django.urls import path
from .views import *

app_name = 'support'
urlpatterns = [
    path('', support_create, name="create"),
]
