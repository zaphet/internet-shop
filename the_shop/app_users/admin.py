from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'second_name', 'phone_number', 'money', 'is_active', 'money_spend']
    list_filter = ['user']
    actions = ['set_active', 'set_not_active']

    def set_active(self, request, queryset):
        queryset.update(is_active='a')

    def set_not_active(self, request, queryset):
        queryset.update(is_active='n')

    set_active.short_description = 'включить пользователя'
    set_not_active.short_description = 'отключить пользователя'
