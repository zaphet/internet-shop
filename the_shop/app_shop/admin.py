from django.contrib import admin
from django.db.utils import ProgrammingError
from .models import ProductCategory, Product, SiteSettings, Shop, ShopToProduct, ProductReview


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active", "sorting_index"]
    list_filter = ["is_active"]
    ordering = ["sorting_index", "name", "is_active"]

    def set_active(self, request, queryset):
        queryset.update(is_active=True)

    def set_not_active(self, request, queryset):
        queryset.update(is_active=False)

    set_active.short_description = 'включить'
    set_not_active.short_description = 'отключить'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "is_active"]
    list_filter = ["is_active"]
    ordering = ["name", "category", "is_active"]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(ShopToProduct)
class ShopToProductAdmin(admin.ModelAdmin):
    list_display = ["id", "shop_id", "product_id", "price", "amount", "discount"]
    list_filter = ["shop_id", "product_id"]
    ordering = ["product_id", "price", "shop_id"]


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "shop_to_product", "created_at", "text"]
    list_filter = ["user", "shop_to_product"]
    ordering = ["created_at", "shop_to_product", "user"]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_url', 'title', 'delivery_price', 'free_delivery_from', 'express_delivery_price']
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            SiteSettings.load().save()
        except ProgrammingError:
            pass

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False
