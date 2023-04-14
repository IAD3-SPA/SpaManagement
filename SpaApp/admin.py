from django.contrib import admin
from .models import Product, ProductDelivery, Storage, User


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductDelivery)
class ProductDeliveryAdmin(admin.ModelAdmin):
    pass


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'type', 'is_active')

