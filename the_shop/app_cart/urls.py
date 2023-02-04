from django.urls import path
from .views import cart_detail, cart_add, cart_remove, CreateOrder, Payment

app_name = "app_cart"

urlpatterns = [
    path('cart_detail/', cart_detail, name='cart'),
    path("cart_add/", cart_add, name='cart_add'),
    path("cart_remove/", cart_remove, name='cart_remove'),
    path("cart_dec/", cart_remove, name='cart_dec'),
    path("create_order/", CreateOrder.as_view(), name='create_order'),
    path("payment/", Payment.as_view(), name='payment'),
]
