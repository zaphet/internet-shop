from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "user", "status", "name", "phone", "mail", "city", "address", "delivery",
                    "pay", "comment", "products", "total_price"]
    list_filter = ['user', "status"]
    ordering = ["created_at", "user", "status", "total_price"]
    actions = ['set_not_paid', 'put_in_queue', 'set_paid', 'set_finished', 'set_canceled']

    def set_not_paid(self, request, queryset):
        queryset.update(status='Не оплачен')

    def put_in_queue(self, request, queryset):
        queryset.update(status='В очереди')

    def set_paid(self, request, queryset):
        queryset.update(status='Оплачен')

    def set_finished(self, request, queryset):
        queryset.update(status='Выполнен')

    def set_canceled(self, request, queryset):
        queryset.update(status='Отменён')

    set_not_paid.short_description = 'сделать не оплаченным'
    put_in_queue.short_description = 'поставить в очередь на оплату'
    set_paid.short_description = 'сделать оплаченным'
    set_finished.short_description = 'сделать законченным'
    set_canceled.short_description = 'сделать отменённым'
