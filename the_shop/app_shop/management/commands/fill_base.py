from django.core.management import BaseCommand
import random
from app_shop.models import ProductCategory, Product, Shop, ShopToProduct

dict_of_words1 = [
    'первый', 'второй', 'третий', 'последний', 'самый последний', 'новый', 'старый', 'зелёный', 'внезапный'
]
dict_of_words2 = [
    'хорошая', 'плохая', 'синяя', 'новая', 'старая', 'зелёная', 'внезапная'
]
dict_of_words3 = [
    'арбикомс', 'артовал', 'кумодрын', 'потровак', 'сумовал', 'октотрёп', 'контополь', 'пентавоз', 'контрвзвесь'
]


class Command(BaseCommand):
    help = 'Заполнить базу магазинами с товарами'

    def handle(self, *args, **options):
        #  -----магазины
        print('создаю магазины...')
        shop_amount = 0

        for word_part in dict_of_words1:
            Shop.objects.create(name=f'{word_part} магазин')
            shop_amount += 1
        #  -----категории
        print('создаю категории товаров...')
        category_amount = 0

        for word_part in dict_of_words2:
            random_num = random.randint(1, 12)
            if random_num % 2 == 0:
                rand_is_active = True
            else:
                rand_is_active = False
            if random_num % 2 == 0:
                rand_index = 1 + random_num / 100
            else:
                rand_index = 1 - random_num / 100
            ProductCategory.objects.create(name=f'{word_part} категория', is_active=rand_is_active
                                           , sorting_index=rand_index)
            category_amount += 1
        #  -----товары
        print('создаю товары...')
        categories = ProductCategory.objects.all()
        product_amount = 0

        for caty in categories:
            for word_part in dict_of_words3:
                random_num = random.randint(1, 12)
                if random_num % 2 == 0:
                    rand_is_active = True
                else:
                    rand_is_active = False
                Product.objects.create(name=f'{word_part}', is_active=rand_is_active, category=caty)
                product_amount += 1
        #  -----предложения
        print('создаю предложения...')
        shops = Shop.objects.all()
        products = Product.objects.all()
        shop_to_product_amount = 0
        for shop in shops:
            for prod in products:
                random_price = random.randint(99, 1999)
                random_num = random.randint(0, 12)
                random_discount = random.randint(0, 30)

                is_limited = False
                rand_index = 1
                if random_num % 2 == 0:
                    rand_index = 1 + random_num / 100
                elif random_num % 3 == 0:
                    is_limited = True
                else:
                    rand_index = 1 - random_num / 100
                description = f'Это автоматически сгенерированное описание товара {prod.name} из магазина {shop.name}.'
                ShopToProduct.objects.create(shop_id=shop, product_id=prod, price=random_price, amount=random_num
                                             , discount=random_discount, sorting_index=rand_index
                                             , is_limited=is_limited, description=description)
                shop_to_product_amount += 1

        self.stdout.write(f'Создано:\n\t{shop_amount} магазинов\n\t{category_amount} категорий\n'
                          f'\t{product_amount} товаров\n\t{shop_to_product_amount} предложений')
