from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login as login_view,login,logout
from .models import Cart,Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from .views import *
from django.urls import reverse

@login_required(login_url='/signin/')
def dasboard(requst):
    all_products = Product.objects.all()

    paginator = Paginator(all_products, 4)  # Paginate with 2 items per page
    page = requst.GET.get('page', 1)  # Get page number from request
    try:
        all_products = paginator.page(page)  # ✅ Correct usage
    except PageNotAnInteger:
        all_products = paginator.page(1)  # ✅ Correct usage
    except EmptyPage:
        all_products = paginator.page(paginator.num_pages)  # ✅ Correct usage

    context = {
        'all_products' : all_products,
    }
    
    return render(requst, 'customer/dasboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('signin')
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username,password=password)
            if user:
                login_view(request, user)
                messages.success(request, 'login successful')
                return redirect('dasboard')
        else:
            messages.error(request, 'Username and password is requeard')
    return render(request, 'customer/account/signin.html')
def signup(request):
   
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confrom_password =request.POST.get('confrom_password')

        if password != confrom_password:
            messages.error(request, 'password do not match')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use')
            return redirect('signup')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                )
            messages.success(request, 'Account created successfuly')
            return redirect('signin')

    return render(request, 'customer/account/signup.html')

@login_required
def card_list(request):
    cards = Cart.objects.all()
    all_products = Product.objects.all()

    paginator = Paginator(all_products, 4)  # Paginate with 2 items per page
    page = request.GET.get('page', 1)  # Get page number from request
    try:
        all_products = paginator.page(page)  # ✅ Correct usage
    except PageNotAnInteger:
        all_products = paginator.page(1)  # ✅ Correct usage
    except EmptyPage:
        all_products = paginator.page(paginator.num_pages)  # ✅ Correct usage
    
    context = {
        'all_products':all_products,
        "cards":cards
    }
   
    return render(request, "customer/cards/card_list.html",context )

@login_required
def add_to_cart(request,product_id):
    
        product = get_object_or_404(Product, id=product_id)
        user = request.user
 
        cart_item, created  = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            # If the item already exists, increase the quantity
            cart_item.quantity += 1
            cart_item.save()

        return redirect('card_list')


def change_password(request, token):
    context = {}
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        if not profile_obj:
            return HttpResponse('Invali Token')
        
        context = {
            'user_id' : profile_obj.user.id
            }
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            conform_password = request.POST.get('conform_password')
            user_id = profile_obj.user.id

            if user_id is  None:
                messages.error(request, 'No user id found.')
                return redirect(reverse('change-password', kwargs={'token': token}))
                
            
            if  new_password != conform_password:
                messages.success(request, 'both should  be equal.')
                return redirect(reverse('change-password', kwargs={'token': token}))
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('sign_in')     
    except Exception as e:
        messages.error(request, f"All fields required!") 

    return render(request, 'customer/account/change_password.html', context)

def forget_password(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        # ইউজার যদি না থাকে, তেমন ক্ষেত্রে মেসেজ দেখানো
        if not User.objects.filter(email=email).first():
            messages.error(request, 'No user found with this email!')
            return redirect('forget_password')
        
        # ইউজারের টোকেন তৈরি করা
        user_obj = User.objects.get(email=email)
        token = str(uuid.uuid4())
        profile_obj = Profile.objects.get(user=user_obj)
        profile_obj.forget_password_token = token
        profile_obj.save()
        print(profile_obj)
        # context সেট করা
        context = {
            'token': token,
            'name': profile_obj
        }

        # send_email ফাংশন কল করা এবং ফলাফল চেক করা
        result = send_email(f"Reset your Password", [email], 'customer/account/reset_password.html', context, [])
        
        # সঠিকভাবে রিটার্ন চেক করার জন্য প্রিন্ট করা
        print(result)  # এটি send_email ফাংশনের আউটপুট হবে

        # ইউজারকে ইমেইল চেক করার জন্য মেসেজ পাঠানো
        messages.success(request, 'Reset your password. Please check your inbox!')
        return redirect('forget_password')

    # GET রিকোয়েস্ট হলে forget-password পেজ রেন্ডার করা
    return render(request, 'customer/account/forget_password.html')

from django.http import HttpResponse
def send_email(request):
        
    subject = "Test Email from Django"
    message = "Hello! This is a test email sent using Django."
    
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # Sender's email (from settings.py)
        ['mdovi0177688@gmail.com'],  # List of recipient emails
        fail_silently=False,  # Set to True in production to avoid errors stopping execution
    )
    return HttpResponse('Email Has been Send.')
        
def verify_email(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print(otp)

        user_otp = Profile.objects.filter(email_verification_code=otp).first()

        if user_otp:
            user = User.objects.get(id=user_otp.user.id)

            if otp == user_otp.email_verification_code:
                login(request, user)
                messages.success(request, "Login successful")
                return redirect('home')
            else:
                messages.error(request, "Invalid OTP entered")
        else:
            messages.error(request, "Invalid OTP entered or user not found")

    return render(request, 'customer/account/verify_email.html')        