from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.db import transaction

from .models import UserProfile
from .forms import AuthForm, RegisterForm, RestorePasswordForm, ChangeProfileForm, AvatarForm
from app_cart.models import Order
from app_shop.models import ShopToProduct


def register_view(request):
    if request.method == 'POST':
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
                return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        next_page = request.GET.get('next', 'main')
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(next_page)
                else:
                    auth_form.add_error('__all__', 'Ошибка! Учётная запись пользователя не активна!')
            else:
                auth_form.add_error('__all__', 'Ошибка! Проверьте правильность написания логина и пароля!')
    else:
        auth_form = AuthForm()
    context = {
        'form': auth_form
    }
    return render(request, 'users/login.html', context=context)


class MyLogoutView(LogoutView):
    next_page = '/'


class AccountView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('main')
        ava = UserProfile.objects.filter(user=request.user).first().avatar
        orders = Order.objects.filter(user=request.user)
        last_order = orders.order_by('-created_at').first()
        context = {'avatar': ava, 'last_order': last_order}
        return render(request, 'users/account.html', context=context)


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('main')

        form = ChangeProfileForm()
        ava_form = AvatarForm()
        context = {'form': form, 'ava_form': ava_form}

        return render(request, 'users/profile.html', context=context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('main')
        user = User.objects.get(id=request.user.id)
        user_profile = UserProfile.objects.filter(user=request.user).first()
        form = ChangeProfileForm(request.POST)
        ava_form = AvatarForm(request.POST, request.FILES)
        if form.is_valid() and ava_form.is_valid():
            names_dict = form.cleaned_data.get('full_name').split()
            user.first_name = names_dict[0].title()
            user.last_name = names_dict[1].title()
            user.email = form.cleaned_data.get('email')
            user.save()
            user_profile.second_name = names_dict[2].title()
            user_profile.phone_number = form.cleaned_data.get('phone_number')
            user_profile.avatar = request.FILES['avatar']
            user_profile.save()
            return redirect('app_users:account')

        context = {'form': form, 'ava_form': ava_form}

        return render(request, 'users/profile.html', context=context)


class OrdersHistoryView(View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        orders = orders.order_by('-created_at')
        context = {'orders': orders}
        return render(request, 'users/orders_history.html', context=context)


class OrdersDetailView(View):
    def get(self, request):
        order_id = request.GET.get('order_id', '')
        if not order_id:
            return redirect('app_users:orders_history')
        order = Order.objects.filter(id=order_id).first()
        order_cart = order.products
        cart_list = []
        products_ids = []
        for item in order_cart.split():
            item_list = item.split(':')
            cart_list.append([int(item_list[0]), int(item_list[1])])
            products_ids.append(int(item_list[0]))
        print(cart_list)
        print(products_ids)
        products = ShopToProduct.objects.filter(id__in=products_ids)
        for product in products:
            print(product.id)

        context = {'order': order, 'cart_list': cart_list, 'products': products}
        return render(request, 'users/one_order.html', context=context)


def restore_password(request):
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            return HttpResponse(f'Новый пароль типа вылетел на {form.cleaned_data["email"]}, '
                                f'но на самом деле нет.')
    form = RestorePasswordForm()
    context = {'form': form}
    return render(request, 'users/restore_password.html', context=context)
