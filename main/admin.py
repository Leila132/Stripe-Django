from django.contrib import admin
from .models import Item, Order, Discount, Tax

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'price')  # Поля, отображаемые в списке заказов
    filter_horizontal = ('items', 'taxes')  # Горизонтальный фильтр для выбора товаров
    readonly_fields = ('price', 'subtotal', 'discount_amount', 'tax_amount')

admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount)
admin.site.register(Tax)