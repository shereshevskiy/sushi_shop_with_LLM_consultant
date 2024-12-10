from django.contrib import admin
from .models import Cart, Item


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    exclude = ('content_type',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
