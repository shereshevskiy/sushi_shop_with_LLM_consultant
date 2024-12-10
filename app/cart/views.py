# views.py
from cart.cart import Cart
from shop.models import Product
from django.shortcuts import render, redirect
from django.http import HttpResponse

def add_to_cart(request, product_id, quantity):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product, product.price, quantity)
    return redirect('cart')


def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart')

def get_cart(request):
    return render(request, 'cart.html', {'cart': Cart(request)})
