from django.contrib import admin

# Register your models here.
from order.models import ShopCart, OrderProduct, Order


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity', 'price','amount']
    list_filter = ['user']

class OrderProductLine(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product', 'price', 'quantity', 'amount')
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'total', 'status','code',]
    list_filter = ['status']
    readonly_fields = ('user', 'address', 'city', 'country', 'phone', 'first_name', 'ip', 'last_name', 'total','code')
    can_delete = False
    inlines = [OrderProductLine]
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'price', 'quantity', 'amount']
    list_filter = ['user']

admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
