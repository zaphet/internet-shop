from django.urls import path

from .views import CatalogView, ProductDetailsView

app_name = "app_shop"

urlpatterns = [
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path("product_details/", ProductDetailsView.as_view(), name="product_details"),
]
