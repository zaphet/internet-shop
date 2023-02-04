from app_shop.models import ProductReview
from django.db import transaction


class Review(object):

    @classmethod
    def add(cls, user, shop_to_product, text):
        """
        добавить отзыв к товару
        """

        with transaction.atomic():
            ProductReview.objects.create(user=user, shop_to_product=shop_to_product, text=text)
            shop_to_product.reviews += 1
            shop_to_product.save()
        return shop_to_product.reviews

    @classmethod
    def get_rewiews(cls, product_id, amount):
        """
        получить список отзывов к товару
        """
        reviews = ProductReview.objects.filter(shop_to_product=product_id)[:amount]
        return reviews

    def get_discount(self):
        """
        получить скидку на корзину
        """
        pass

    @classmethod
    def get_rewiews_amount(cls, product_id):
        """
        получить количество отзывов для товара

        """
        reviews_amount = ProductReview.objects.filter(shop_to_product=product_id)
        return len(reviews_amount)
