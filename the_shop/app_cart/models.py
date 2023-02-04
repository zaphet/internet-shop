from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    status = models.CharField(max_length=20, default='Не оплачен', verbose_name='Статус заказа')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    phone = models.CharField(max_length=12, verbose_name='Номер телефона')
    mail = models.EmailField(max_length=50, verbose_name='Имэйл')
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=300, verbose_name='Адрес')
    delivery = models.CharField(max_length=100, verbose_name='Тип доставки')
    pay = models.CharField(max_length=100, verbose_name='Тип оплаты')
    comment = models.TextField(max_length=1000, blank=True, default='', verbose_name='Комментарий к заказу')
    products = models.TextField(null=False, blank=True, default='', verbose_name='Список товаров')
    total_price = models.IntegerField(default=0, verbose_name='Сумма заказа')
    error = models.CharField(max_length=100, blank=True, default='', verbose_name='Текст ошибки')

    def __str__(self):
        return f'{self.created_at} {self.user} {self.status} '

    class Meta:
        db_table = 'orders'
        ordering = ['created_at', 'status']
