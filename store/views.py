from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserInfoForm
from django.db.models import Q
from cart.cart import Cart 
import json 
from payment.forms import ShippingForm
from payment.models import ShippingAddress


# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products' :products})

def about(request):
    return render(request, 'about.html')

def signin_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            current_user = Profile.objects.get(user__id=request.user.id)
            
            saved_cart = current_user.old_cart
            
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                
                cart = Cart(request)
                
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            
            
            
            messages.success(request, ("You have been sucessfully log in "))
            return redirect('home')
        else:
            messages.success(request, ("Your username or password not matching"))
            return redirect('signin')
            
     
    else:   
        return render(request, 'signin.html')

def signout_user(request):
    logout(request)
    messages.success(request, "You Have been Log Out Sucessfully.... ")
    return redirect ('home')

def signup_user(request):
    if request.method =='POST':
        fn = request.POST['first_name']  
        ln = request.POST['last_name']    
        email = request.POST['email']   
        username = request.POST['username']   
        pwd1 =request.POST['psw'] 
        pwd2 =request.POST['psw-repeat']
        
        if pwd1 == pwd2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Id Already Used")
                return render(request, 'signup.html')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Exist ")
                return render(request, 'signup.html')
            else:
                user = User.objects.create_user(username=username , password=pwd1 , first_name=fn, last_name = ln,email=email)
                user.save()
                user = authenticate(username=username, password=pwd1)
                login(request, user)
			    
                messages.success(request, "Please Fill your Personal Info.... ")
                return redirect('update_info')
        else:
            messages.info(request, "Password did not match ")
            return render(request, 'signup.html')
            
    else:
        return render(request, 'signup.html')
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def category(request, foo):
    category = Category.objects.get(name=foo)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'products':products, 'category':category})

def category_summery(request):
    categorys = Category.objects.all()
    return render(request, 'category_summery.html', {'categorys':categorys})





@login_required
def user_update(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        
        if first_name and last_name and email and username:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('home')  # Redirect to a profile page or another page after successful update
    else:
        current_user = request.user

    return render(request, 'user_update.html', {
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
        'username': current_user.username,
    })
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your Info Has Been Updated!!")
            return redirect('home')
        return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!!")
        return redirect('home')
        
        
def search(request):
    if request.method == "POST":
        
        searched = request.POST['searched']
        
        
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        
        if not searched:
            messages.success(request, "This product does not exist... sorry!!")
            return render(request, 'search.html')
        
        else:
            return render(request, "search.html", {'searched':searched})
    else:
        return render(request, 'search.html')
    
def new(request):
    return render (request, 'new.html')

    