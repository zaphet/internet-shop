from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Min, Max

from .models import ShopToProduct, Product
from .services.reviews import Review


class TestView(View):
    def get(self, request):
        return render(request, 'test.html')


class MainView(View):
    def get(self, request):

        popular_products = ShopToProduct.objects.order_by('-sorting_index', '-sold')[:8]
        limited_products = ShopToProduct.objects.filter(is_limited=True)[:16]

        return render(request, 'main.html', {'popular_products': popular_products, 'limited_products': limited_products})


class CatalogView(View):

    def get(self, request):
        products = ShopToProduct.objects.all()
        # -----фильтрация категория
        category = request.GET.get('category', '')
        if category:
            product_ids = Product.objects.filter(category=category)
            products = products.filter(product_id__in=product_ids)
        # -----фильтрация цена
        price_stats = products.aggregate(Max('price'), Min('price'))
        price_min = price_stats['price__min']
        price_max = price_stats['price__max']
        price_from = request.GET.get('price_from', price_min)
        price_to = request.GET.get('price_to', price_max)
        products = products.filter(price__gt=price_from, price__lt=price_to)
        # -----фильтрация название
        product_name = request.GET.get('product_name', 'Название')
        if product_name != 'Название':
            product_ids = Product.objects.filter(name__contains=product_name)
            products = products.filter(product_id__in=product_ids)
        # -----фильтрация наличие
        in_stock = request.GET.get('in_stock', 'on')
        if in_stock == 'on':
            products = products.filter(amount__gt=0)
        # -----фильтрация доставка
        free_shipping = request.GET.get('free_shipping', 'None')
        if free_shipping == 'on':
            # products = products.filter(free_shipping=True)
            pass
        # -----сортировка
        order = request.GET.get('order', 'sold')
        if order not in ['sold', '-sold', 'price', '-price', 'reviews', '-reviews', 'created_at', '-created_at']:
            order = 'sold'
        products = products.order_by(order)
        # -----пагинация
        paginator = Paginator(products, 8)
        page_number = request.GET.get('page', '1')
        products_page = paginator.get_page(page_number)

        return render(request, 'shop/catalog.html', {
            'paginator': paginator, 'products': products_page,
            'category': category, 'order': order,
            'price_min': price_min, 'price_max': price_max, 'price_from': price_from, 'price_to': price_to,
            'product_name': product_name,
            'in_stock': in_stock, 'free_shipping': free_shipping
        })

    def post(self, request):
        url = f'/shop/catalog/?'
        # -----фильтрация категория
        category = request.GET.get('category', '')
        if category:
            url += f'category={category}&'
        # -----фильтрация цена
        price_stats = request.POST.get('price')
        if price_stats:
            # print(price_stats)  # 551;1991
            price_from = price_stats.split(';')[0]
            price_to = price_stats.split(';')[1]
            # print(price_from, price_to)  # 551 1991
            url += f'price_from={price_from}&price_to={price_to}&'
            # -----фильтрация название
        product_name = request.POST.get('title')
        if not product_name:
            product_name = request.GET.get('product_name', 'Название')
        url += f'product_name={product_name}&'
        # -----фильтрация наличие
        in_stock = request.POST.get('in_stock_box')
        # print(in_stock)  # on
        url += f'in_stock={in_stock}&'
        # -----фильтрация доставка
        free_shipping = request.POST.get('free_shipping_box')
        if free_shipping:
            # print(free_shipping)  # None
            url += f'free_shipping={free_shipping}&'
        # -----сортировка
        order = request.GET.get('order', 'sold')
        if order:
            url += f'order={order}&'
        # -----пагинация
        page_number = request.GET.get('page', '1')
        if page_number:
            url += f'page_number={page_number}&'

        url = url[:-1]
        # url = f'/shop/catalog/?category={category}&in_stock={in_stock}&free_shipping={free_shipping}' \
        #       f'&product_name={product_name}&price_from={price_from}&price_to={price_to}&order={order}' \
        #       f'&page={page_number}'
        return redirect(url)


class ProductDetailsView(View):

    def get(self, request):
        product_id = request.GET.get('product', '')
        reviews_amount = int(request.GET.get('reviews_amount', 4))
        if not product_id:
            return redirect('app_shop:catalog')
        product = ShopToProduct.objects.filter(id=product_id).first()
        reviews = Review.get_rewiews(product_id=product_id, amount=reviews_amount)

        return render(request, 'shop/product.html', {
            'product': product, 'reviews': reviews, 'reviews_amount': reviews_amount
        })

    def post(self, request):
        product_id = request.GET.get('product', '')
        reviews_amount = int(request.GET.get('reviews_amount', 4))
        if not product_id:
            return redirect('app_shop:catalog')
        product = ShopToProduct.objects.filter(id=product_id).first()
        reviews = Review.get_rewiews(product_id=product_id, amount=reviews_amount)

        review_text = request.POST.get('review')
        if review_text:
            Review.add(user=request.user, shop_to_product=product, text=review_text)
        return render(request, 'shop/product.html', {
            'product': product, 'reviews': reviews, 'reviews_amount': reviews_amount
        })
