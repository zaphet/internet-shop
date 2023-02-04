from django.urls import path

from .views import login_view, MyLogoutView, register_view, AccountView, ProfileView, restore_password, OrdersHistoryView, OrdersDetailView

app_name = "app_users"

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('account/', AccountView.as_view(), name='account'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('orders_history/', OrdersHistoryView.as_view(), name='orders_history'),
    path('order_detail/', OrdersDetailView.as_view(), name='order_detail'),
    path('restore_password/', restore_password, name='restore_password'),
]
