from django.urls import path
from . import views  # views = arquivo que contém os endpoints

urlpatterns = [
    # Quando a URL raiz do app for acessada (''), chame a view 'product_list'.
    # O 'name' é um apelido útil para usarmos nos templates.
    path("", views.product_list, name="product_list"),  # Página inicial que lista os produtos
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('update-cart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
    # Novas URLs
    path('clear-session/', views.clear_session, name='clear_session'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cadastro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout_view, name='checkout'),
]
