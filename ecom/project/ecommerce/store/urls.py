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
    #authentication url
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    #frontend url
    path('', views.store, name='store'),
    path('about/', views.about, name='about'),
    path('<int:pk>/detail', views.detail, name='item_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('updateItem/', views.updateItem, name='update_item'),
    path('search_product/', views.searchItem, name='search_item'),
    
    #backend url
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:pk>/password_change', views.password_change, name='password_change'),
    path('products/', views.products, name='products'),
    path('add_product/', views.add_product, name='add_product'),
    path('<int:pk>/delete_product', views.delete_product, name='delete_product'),
    path('<int:pk>/edit_product', views.edit_product, name='edit_product'),
    path('<int:pk>/update_profile', views.update_profile, name='update_profile'),
    path('order_list', views.orderList, name='order_list'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
