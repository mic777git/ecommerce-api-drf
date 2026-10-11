from django.contrib import admin
from .models import Category, Product, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'created_at')
    inlines = [OrderItemInline]


admin.site.register(Category)
admin.site.register(Product)
