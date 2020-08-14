from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json

""" frontend views """

# home page.
def store(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}

    products = Product.objects.all()
    context = {'products':products, 'order':order }
    return render(request, 'store/store.html', context)

# about page.
def about(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}

    products = Product.objects.all()
    context = {'products':products, 'order':order }
    return render(request, 'store/about.html', context)    

# single product detail page.
def detail(request, pk):
    product = Product.objects.get(pk=pk)
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}

    context = {'product':product, 'order':order }
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


""" get called when add to cart event is initiated, get product id 
and action type from request body and update the quantity of individual product. """
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    productAction = data['productAction']
    customer = Customer.objects.get(user=request.user)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False) 
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) 
    
    if productAction == 'add':
        orderItem.quantity += 1
    elif productAction == 'remove': 
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity < 0:
        orderItem.delete()

    return JsonResponse('item added', safe=False)     
    