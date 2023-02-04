from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from django.db import transaction

from app_users.models import UserProfile
from app_users.forms import RegisterForm
from app_shop.models import ShopToProduct, SiteSettings
from .services.shopping_cart import Cart
from .services.payment_integrate_sevice import job
from .forms import CerateOrderForm
from .models import Order


def cart_add(request):
    cart = Cart(request)
    product = get_object_or_404(ShopToProduct, id=request.GET.get('product', ''))
    amount = int(request.GET.get('amount', 1))
    cart.add(product=product, quantity=amount)
    return redirect('app_cart:cart')


def cart_remove(request):
    cart = Cart(request)
    product = get_object_or_404(ShopToProduct, id=request.GET.get('product', ''))
    cart.remove(product)
    return redirect('app_cart:cart')


def cart_detail(request):
    cart = Cart(request)

    return render(request, 'cart/cart.html', {'cart': cart})


def make_products_string(cart):
    cart_total_price = 0
    cart_string = ''
    for item in cart:
        cart_string += f'{item["product"].id}:{item["quantity"]} '
        cart_total_price += item['price'] * item['quantity']
    return cart_string


class CreateOrder(View):

    def get(self, request):
        cart = Cart(request)
        if not request.user.is_authenticated:
            form = RegisterForm()
            context = {'form': form}
        else:
            form = CerateOrderForm()
            context = {'cart': cart, 'form': form}
        return render(request, 'cart/order.html', context=context)

    def post(self, request):
        cart = Cart(request)
        if 'register' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    user = form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    login(request, user)
                    phone_number = form.cleaned_data.get('phone_number')

                    names_dict = form.cleaned_data.get('full_name').split()
                    user.first_name = names_dict[0].title()
                    user.last_name = names_dict[1].title()
                    user.save()
                    user.groups.add(Group.objects.get(name='Покупатель'))

                    UserProfile.objects.create(
                        user=user,
                        second_name=names_dict[2].title(),
                        phone_number=phone_number
                    )
                    return redirect('app_cart:create_order')
            else:
                context = {'form': form}
        elif 'create_order' in request.POST:
            form = CerateOrderForm(request.POST)  # name;phone;mail;city;address;delivery;pay;comment
            if form.is_valid():
                with transaction.atomic():
                    site_settings = SiteSettings.objects.first()
                    delivery_type = form.cleaned_data.get('delivery')
                    total_price = Cart.get_total_price(cart)  # site_settings.cache
                    if delivery_type == 'Обычная доставка' and total_price < site_settings.free_delivery_from:
                        total_price += site_settings.delivery_price
                    elif delivery_type == 'Экспресс доставка':
                        total_price += site_settings.express_delivery_price

                    order = Order.objects.create(
                        user=request.user,
                        name=form.cleaned_data.get('name'),
                        phone=form.cleaned_data.get('phone'),
                        mail=form.cleaned_data.get('mail'),
                        city=form.cleaned_data.get('city'),
                        address=form.cleaned_data.get('address'),
                        delivery=delivery_type,
                        pay=form.cleaned_data.get('pay'),
                        comment=form.cleaned_data.get('comment'),
                        products=make_products_string(cart),
                        total_price=total_price
                    )
                    Cart.clear(cart)
                url = f'/cart/payment/?order_id={order.id}&pay_type={order.pay}'
                print(url)
                return redirect(url)

            context = {'cart': cart, 'form': form}

        else:
            context = {'test': 'test'}
        return render(request, 'cart/order.html', context=context)


class Payment(View):

    def get(self, request):
        order_id = request.GET.get('order_id', '')
        pay_type = request.GET.get('pay_type', '')
        if not order_id or not pay_type:
            return redirect('app_users:account')
        context = {'order_id': order_id, 'pay_type': pay_type}
        return render(request, 'cart/payment.html', context=context)

    def post(self, request):
        order_id = request.POST.get('order_id')
        order = Order.objects.filter(id=order_id).first()
        card = request.POST.get('numero1')
        numero_list = str(card).split()
        numero_str = str(numero_list[0]) + str(numero_list[1])
        card = int(numero_str)
        order.status = 'В очереди'

        mess = job(card=card, order_id=order_id)
        print(mess)
        return redirect('app_users:account')
