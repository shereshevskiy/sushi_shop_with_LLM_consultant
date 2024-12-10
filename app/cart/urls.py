from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:product_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.get_cart, name='cart'),
]