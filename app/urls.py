from django.urls import path
from . import views, api  # api = arquivo que contém os endpoints

urlpatterns = [
    path("", views.index, name="index_for_api"),
    path("api/products/", api.get_products, name="get_products"),
    path("api/cart/<int:user_id>/", api.cart, name="cart"),
    path("api/checkout/<int:user_id>/", api.checkout, name="checkout"),
]
