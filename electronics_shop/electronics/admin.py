# admin.py
from django.contrib import admin
from .models import Product, Category, Order, Review, Customer


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('customer', 'product', 'quantity', 'ordered_at')
#     ordering = ('-ordered_at',)

admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Customer)
