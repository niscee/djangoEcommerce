from django.shortcuts import render
from .models import *

""" frontend views """

# landing page.
def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)

# about page.
def about(request):
    context = {}
    return render(request, 'store/about.html', context)    

# single product detail page.
def detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product':product}
    return render(request, 'store/detail.html', context)

# cart detail page.
def cart(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = [] 
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}
    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)


# checkout page.
def checkout(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = [] 
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}
    context = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', context)