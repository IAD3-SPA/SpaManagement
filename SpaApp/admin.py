from django.contrib import admin

from .models import Product, ProductDelivery, Storage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductDelivery)
class ProductDeliveryAdmin(admin.ModelAdmin):
    pass


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    pass
