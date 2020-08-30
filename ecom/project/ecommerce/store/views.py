from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import *
from .form import LoginForm, ProductForm, RegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import page_access
import json

""" List of frontend controller """
# home page.
def store(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}
  
    products = Product.objects.all()
    context = {'products':products, 'order':order }
    return render(request, 'store/frontend/store.html', context)

# search item.
def searchItem(request):
    item_name = request.GET.get('search')
    products = Product.objects.filter(name__contains=item_name)
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}

    context = {'products':products, 'order':order }
    return render(request, 'store/frontend/search.html', context)

# sort item by price highest first.
def sortPriceHighest(request):
    products = Product.objects.order_by('-price')
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}

    context = {'products':products, 'order':order }
    return render(request, 'store/frontend/search.html', context)

# sort item by recent data first.
def sortProductLatest(request):
    products = Product.objects.order_by('-id')
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}

    context = {'products':products, 'order':order }
    return render(request, 'store/frontend/search.html', context)


# sort item by price Lowest first.
def sortPriceLowest(request):
    products = Product.objects.order_by('price')
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
    else:
        order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}

    context = {'products':products, 'order':order }
    return render(request, 'store/frontend/search.html', context)



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


# order store.
def checkoutForm(request):
    if request.user.is_authenticated:
        address = request.POST.get('address')
        city = request.POST.get('city')
        order = Order.objects.get(user=request.user, complete=False)
        form = ShippingAddress(user=request.user, order=order, address=address, city=city)
        form.save()
        order.complete = True
        order.save()
        
  
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
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, user=request.user) 
    
    if productAction == 'add':
        orderItem.quantity += 1
    elif productAction == 'remove': 
        orderItem.quantity -= 1
    
    orderItem.save()

    if orderItem.quantity < 1:
        orderItem.delete()

    return JsonResponse('item added', safe=False)  





""" List of authentication controller """
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
            user = form.save()
            
            #assigning each new user to customer group
            group = Group.objects.get(name="customer")
            user.groups.add(group)

            messages.success(request, 'Your account has been created.')
            return redirect('login')
            
    order = {'get_cartTotalItems':0, 'get_cartTotalPrice':0}
    context = {'form':form , 'order':order}
    return render(request, 'store/authentication/register.html', context) 


#logout user
def logout_view(request):
    logout(request)
    return redirect('store')



""" List of backend controller """  
#order list page.   
@login_required(login_url='/login/')  
def orderList(request):
    try:
        # order = Order.objects.get(user=request.user, complete=True)
        items = OrderItem.objects.filter(user=request.user)
        context = { 'items':items }
        return render(request, 'store/backend/orderhistory.html', context)
    except:
        context = {}
        return render(request, 'store/backend/orderhistory.html', context) 

#dashboard home page   
@login_required(login_url='/login/')  
def dashboard(request):
    context = {}
    return render(request,'store/backend/welcome.html', context)


#change password page.
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
                messages.warning(request, 'credentials didnt match!!')
            
            form = PasswordChangeForm(request.user)
            context = { 'form':form }
            return render(request, 'store/backend/password_change.html', context)

        except:
            return redirect('dashboard')
    else:
        return redirect('store')


#product list page.   
@login_required(login_url='/login/') 
@page_access(allowed=['manager','store assistant'])     
def products(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/backend/products.html', context)


#new product add page.   
@login_required(login_url='/login/') 
@page_access(allowed=['manager','store assistant'])   
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products')
    form = ProductForm()
    context = {'form':form}
    return render(request, 'store/backend/add_product.html', context) 


#product delete function.   
@login_required(login_url='/login/') 
@page_access(allowed=['manager','store assistant'])   
def delete_product(request, pk):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            return redirect('products')
        except:
            messages.warning(request, 'something went wrong!!')
        return redirect('products')    


#update product.   
@login_required(login_url='/login/') 
@page_access(allowed=['manager','store assistant'])   
def edit_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product has been updated!!')
            return redirect('products')
    form = ProductForm(instance=product)
    context = {'form':form}
    return render(request, 'store/backend/add_product.html', context) 


#update profile.
@login_required(login_url='/login/')  
def update_profile(request, pk):
    if request.method == "POST":
        user_profile = Profile.objects.get(user=pk)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=user_profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully!!')

    user_profile = Profile.objects.get(user=pk)
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=user_profile)
    context = {'user_form':user_form, 'profile_form':profile_form}
    return render(request, 'store/backend/update_profile.html', context)    
                
           
        
       
    