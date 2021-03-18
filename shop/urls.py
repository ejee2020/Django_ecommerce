from django.contrib import admin
from .views import *
from django.urls import path

app_name = 'shop'
urlpatterns = [
    path('', product_in_category, name="product_all"),
    path('sort/<slug:sort_slug>/', sort_in_slug, name="sort_in_slug"),
    path('category/<slug:category_slug>/',
         product_in_category, name="product_in_category"),
    path('<int:id>/<product_slug>/', product_detail,
         name="product_detail"),
    path('search', search_bar, name='search'),
    path('filter',
         filter, name='filter2'),
    path('filter2', FilterAjaxView.as_view(), name='filter_ajax'),
    path('put/<int:id>', put_into_wishlist, name='put_into_wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('remove/<int:id>', remove_from_wishlist, name='remove_from_wishlist'),
    path('create_support', create_support, name='create_support'),
    path('supportlist/', supportlist, name='supportlist'),
    path('paypal/<str:order>', paypal, name='paypal'),
    path('redirect/', redirect, name='redirect'),
    path('completeOrder', completeOrder, name='completeOrder'),
    path('review_write/<int:product_id>', review_write, name='review_write'),
    path('create_review', create_review, name='create_review'),
    path('review_detail/<int:review_id>', review_detail, name='review_detail'),
    path('support_detail/<int:support_id>',
         support_detail, name='support_detail'),
    path('orders',
         orders, name='orders'),
    path('settings',
         settings, name='settings'),

]
