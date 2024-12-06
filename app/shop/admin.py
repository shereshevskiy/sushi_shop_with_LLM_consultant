from django.contrib import admin

# Register your models here.
from django.contrib import admin
from shop.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ['id', 'name', 'price', 'image']
    list_editable = ['name', 'price', 'image']
