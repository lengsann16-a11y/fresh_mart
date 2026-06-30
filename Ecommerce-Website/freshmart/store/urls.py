from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_list, name='order_list'),

    # Auth
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    # Profile & Contact
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    # Add these paths inside your urlpatterns in store/urls.py

    # Product Management (CRUD)
    path('manage/product/add/', views.product_create, name='product_create'),
    path('manage/product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('manage/product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
]



