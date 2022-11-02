from django.contrib import admin

from .models import Item, OrderItem, Order, Address

from import_export import resources
from import_export.fields import Field
from import_export.admin import ExportActionMixin


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        fields = ('title', 'price', 'details')


class ItemModelAdmin(ExportActionMixin,admin.ModelAdmin):
    fields = ('title', 'price','details')
    resource_class = ItemResource


class OrderAdmin(admin.ModelAdmin):

    list_display = ('user', 'ordered')


admin.site.register(Item, ItemModelAdmin)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address)
