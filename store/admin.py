from typing import Any, List, Optional, Tuple
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models




class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)
        


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['collection']
    exclude = ['promotion']
    prepopulated_fields = {
        'slug':['title']
    }
    actions = ['clear_inventory']
    list_display = ['title','unit_price', 'inventory_status','collection_title']
    list_per_page = 20 
    list_filter = ['collection','last_update', InventoryFilter]
    list_select_related = ['collection']
    
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} product were successfully updated!!!",
            messages.ERROR
        )

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name',"last_name",'membership']
    list_editable = ['membership']
    ordering = ['first_name','last_name']
    list_per_page = 20 
    search_fields = ["first_name","last_name"] 


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem    
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id',"placed_at",'customer']


class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title','products_count']

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = reverse('admin:store_product_changelist') + "?" + urlencode({'collection__id':str(collection.id)})
        return format_html('<a href="{}" >{}</a>',url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        ) 
# Register your models here.
admin.site.register(models.Order,OrderAdmin)
admin.site.register(models.Collection,CollectionAdmin)
admin.site.register(models.Product,ProductAdmin)
admin.site.register(models.Customer,CustomerAdmin)
