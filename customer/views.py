from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login as login_view,logout
from .models import Cart,Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.conf import settings
from .models import PasswordResetToken







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


def forgot_password(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        if not email:
            messages.error(request, 'Email field is required.')
            return redirect('forgot_password')
        try:
            user = User.objects.get(email=email)
            print(user)
            token = get_random_string(50)

            PasswordResetToken.objects.filter(user=user).delete()
            PasswordResetToken.objects.create(user=user, token=token)
            
            reset_link = f"{settings.SITE_URL}/reset_password/{token}/"

            send_mail(
                'Reset Your Password',
                f'Click this link to reset your password: {reset_link}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            print('sent')

            messages.success(request, 'Check your email for the reset link.')
            return redirect('signin')

        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
            return redirect('forgot_password')

    return render(request, 'customer/account/forgot_password.html')

def reset_password(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        user = reset_token.user
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid token.')
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password')
        confrom_password = request.POST.get('confrom_password')

        if password != confrom_password:
            messages.error(request, 'Passwords do not match.')
            return redirect(f'/reset_password/{token}/')
        
        if len(password) < 8:  # Simple password length check
           messages.error(request, 'Password must be at least 8 characters long.')
           return redirect(f'/reset_password/{token}/')

        user.password = make_password(password)
        user.save()
        reset_token.delete()

        messages.success(request, 'Password reset successfully. Please log in.')
        return redirect('signin')

    return render(request, 'customer/account/reset_password.html', {'token': token})




def pass_reset_complete(request):
    
    return render(request, 'customer/account/pass_reset_complete.html')
def pass_reset_confirm(request):
    
    return render(request, 'customer/account/pass_reset_confirm.html')

def change_password(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to change your password.')
        return redirect('login')
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confrom_password = request.POST.get('confrom_password')

        # Check if passwords match
        if new_password != confrom_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('change_password')  # Redirect back to the same page

        # Check password length (optional)
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('change_password')

        # Get the current user (assuming the user is logged in)
        if request.user.is_authenticated:
            user = request.user
            user.password = make_password(new_password)  # Hash the new password
            user.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, 'You must be logged in to change your password.')
            return redirect('login')

    return render(request, 'customer/account/change_password.html')


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
        