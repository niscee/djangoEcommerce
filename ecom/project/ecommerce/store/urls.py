"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    # (authentication_urls)
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    
    # (frontend_urls)

    # home page url.
    path('', views.store, name='store'),

    # about page url.
    path('about/', views.about, name='about'),

    # individual product page url.
    path('<int:pk>/detail', views.detail, name='item_detail'),

    # cart page url.
    path('cart/', views.cart, name='cart'),

    # checkout page url.
    path('checkout/', views.checkout, name='checkout'),

    # cart-item[add, delete, update, availability ] url.
    path('updateItem/', views.updateItem, name='update_item'),

    # search page url.
    path('search_product/', views.searchItem, name='search_item'),

    # final order submit page url.
    path('checkout_form/', views.checkoutForm, name='checkout_form'),

    # sort product based on price desc url.
    path('sort_price_highest/', views.sortPriceHighest, name='sortPriceHighest'),

    # sort product based on price asce url.
    path('sort_price_lowest/', views.sortPriceLowest, name='sortPriceLowest'),

    # sort price based on latest product url.
    path('sort_product_latest/', views.sortProductLatest, name='sortProductLatest'),

    
    # (backend_urls)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:pk>/password_change', views.password_change, name='password_change'),
    path('products/', views.products, name='products'),
    path('add_product/', views.add_product, name='add_product'),
    path('<int:pk>/delete_product', views.delete_product, name='delete_product'),
    path('<int:pk>/edit_product', views.edit_product, name='edit_product'),
    path('<int:pk>/update_profile', views.update_profile, name='update_profile'),
    path('contact_manager', views.contactManager, name='contact_manager'),
    path('email', views.emailManager, name='email_manager'),

    # order history of individual customer url.
    path('order_list', views.orderList, name='order_list'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
