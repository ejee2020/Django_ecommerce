from django.urls import path, include
from .views import *
app_name = "order"
urlpatterns = [
    path('create/', order_create, name="order_create"),
    path('create/ajax', OrderCreateAjaxView.as_view(), name='order_create_ajax'),
    path('checkout/', OrderCheckoutAjaxView.as_view(), name='order_checkout'),
    path('validation/', OrderImpAjaxView.as_view(), name='order_validation'),
    path('complete/', order_complete, name='order_complete'),
    path('order_detail/<int:order_id>/',
         admin_order_detail, name='admin_order_detail'),
]
