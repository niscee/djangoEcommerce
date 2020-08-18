from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .form import RegisterForm
from .form import LoginForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import json
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

""" frontend controller """
# home page.
def store(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}
  
    products = Product.objects.all()
    context = {'products':products, 'order':order }
    return render(request, 'store/frontend/store.html', context)


# about page.
def about(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}

    products = Product.objects.all()
    context = {'products':products, 'order':order }
    return render(request, 'store/frontend/about.html', context)    


# single product detail page.
def detail(request, pk):
    product = Product.objects.get(id=pk)
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}

    context = {'product':product, 'order':order }
    return render(request, 'store/frontend/detail.html', context)


# cart detail page.
def cart(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.orderitem_set.all()
    else:
        items = [] 
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}
    context = {'items':items, 'order':order}
    return render(request, 'store/frontend/cart.html', context)



# checkout page.
def checkout(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.orderitem_set.all()
    else:
        items = [] 
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}
    context = {'items':items, 'order':order}
    return render(request, 'store/frontend/checkout.html', context)
    


""" get called when 'add to cart event is initiated, get product id 
and action type from request body and update the quantity of individual product. """
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    productAction = data['productAction']
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=request.user, complete=False) 
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) 
    
    if productAction == 'add':
        orderItem.quantity += 1
    elif productAction == 'remove': 
        orderItem.quantity -= 1
    
    orderItem.save()

    if orderItem.quantity < 1:
        orderItem.delete()

    return JsonResponse('item added', safe=False)     



""" authentication controller """
#login user
def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request, 'credentials didnt match.')
    order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}
    context = {'form':form , 'order':order}
    return render(request, 'store/authentication/login.html', context)


#register new account
def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created.')
            return redirect('login')
            
    order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}
    context = {'form':form , 'order':order}
    return render(request, 'store/authentication/register.html', context) 


#logout user
def logout_view(request):
    logout(request)
    return redirect('store')



""" backend controller """  
#dashboard home page   
@login_required(login_url='/login/')     
def dashboard(request):
    try:
        order = Order.objects.get(user=request.user)
        items = order.orderitem_set.all().order_by('date_added')
        context = {'order':order, 'items':items }
        return render(request, 'store/backend/orderhistory.html', context)
    except:
        context = {}
        return render(request, 'store/backend/orderhistory.html', context) 


#password_change page.
@login_required(login_url='/login/')     
def password_change(request, pk):
    if request.user.id == pk:
        try:
            user = User.objects.get(id=pk)
            if request.method == 'POST':
                form = PasswordChangeForm(request.user, request.POST)
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)  
                    messages.success(request, 'Your password was successfully updated!')
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'Please correct the error below.')
            
            form = PasswordChangeForm(request.user)
            context = { 'form':form }
            return render(request, 'store/backend/password_change.html', context)

        except:
            return redirect('dashboard')
    else:
        return redirect('store')            
        
       
    