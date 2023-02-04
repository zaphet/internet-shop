from django.db import models

from .services.get_admin_settings import AdminSettings
from app_users.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='название категории')
    icon = models.FileField(upload_to='assets/img/icons/departments/', default='assets/img/icons/departments/no_image.svg', verbose_name='файл иконки')
    is_active = models.BooleanField(default=False, verbose_name='активность')
    sorting_index = models.DecimalField(default=1, max_digits=8, decimal_places=2, verbose_name='индекс сортировки')

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='название товара')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, default=None, null=True, related_name='products', verbose_name='категория товара')
    is_active = models.BooleanField(default=False, verbose_name='активность')

    def __str__(self):
        return f'{self.name}({self.category})'


class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name='название магазина')

    def __str__(self):
        return f'{self.name}'


class ShopToProduct(models.Model):
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, default=None, null=True, verbose_name='магазин')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, null=True, verbose_name='товар')
    icon = models.FileField(upload_to='assets/img/content/home/', default='assets/img/content/home/no_image.jpg', verbose_name='файл иконки')
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='цена')
    amount = models.IntegerField(default=0, verbose_name='в наличии')
    discount = models.SmallIntegerField(default=0, verbose_name='скидка')
    sold = models.IntegerField(default=0, verbose_name='продано')
    reviews = models.IntegerField(default=0, verbose_name='обзоров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    sorting_index = models.DecimalField(default=1, max_digits=8, decimal_places=2, verbose_name='индекс сортировки')
    description = models.TextField(max_length=1000, default='', verbose_name='краткое описание товара')
    is_limited = models.BooleanField(default=False, verbose_name='ограниченный тираж»')

    def __str__(self):
        return f'{self.shop_id.name} {self.product_id.name} {self.price} '


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')
    shop_to_product = models.ForeignKey(ShopToProduct, on_delete=models.CASCADE, verbose_name='товар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    text = models.TextField(max_length=1000, default='', verbose_name='текст отзыва')


class SiteSettings(AdminSettings):
    site_url = models.URLField(max_length=256, verbose_name='url сайта')
    title = models.CharField(max_length=256, verbose_name='название сайта')
    cache = models.IntegerField(default=86400, verbose_name='время жизни кэша(сек)')
    delivery_price = models.IntegerField(default=200, verbose_name='стоимость доставки(руб)')
    free_delivery_from = models.IntegerField(default=2000, verbose_name='порог бесплатной доставки(руб)')
    express_delivery_price = models.IntegerField(default=500, verbose_name='стоимость экспресс доставки(руб)')

    def __str__(self):
        return 'Configuration'
