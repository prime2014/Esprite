from django.contrib import admin
from .models import Cart, Order


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'quantity', 'price', 'item', 'created')
    list_filter = ('created',)
    date_hierarchy = "created"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered', 'total_amount', 'vat_tax', 'firstname',
                    'lastname', 'email', 'phone', 'address_1', 'address_2', 'state', 'created')
    list_filter = ("created",)
    filter_horizontal = ('orderedproduct',)
    date_hierarchy = "created"
