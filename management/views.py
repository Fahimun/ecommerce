from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




@login_required(login_url='/signin/')
def index(request):
    
    return render(request,'management/index.html')

def profile(request):
     return render(request, 'management/profile.html')
  
def contacts(request):

    contacts = Contact.objects.all().order_by('-id')
    Search = request.GET.get('Search')
    if Search:
       contacts = Contact.objects.filter( Q(name__icontains = Search) | Q(phone=Search))
   

    context = {
       'contact':contacts
  

    }
    return render(request, 'management/contact_side/contacts.html', context)
def add_contact(request):
    if request.method == 'POST':
     name = request.POST.get('name')
     age = request.POST.get('age')
     phone = request.POST.get('phone')
     address = request.POST.get('address')
    #  print(name,age,phone,address)
     if name and age and phone and address:
       Contact.objects.create(
           name=name,
           age=age,
           phone=phone,
           address=address
       )
       messages.success(request, f"contact {name} added successful")
       return redirect('contacts')
     else:
        messages.error(request, f"contact {name} not added")

    return render(request,'management/contact_side/add_contact.html')

def products(request):
    search_query = request.GET.get('search_query', '')
    all_products = Product.objects.filter(product_name__icontains=search_query,)


    paginator = Paginator(all_products, 4)  # Paginate with 2 items per page
    page = request.GET.get('page', 1)  # Get page number from request
    try:
        all_products = paginator.page(page)  # ✅ Correct usage
    except PageNotAnInteger:
        all_products = paginator.page(1)  # ✅ Correct usage
    except EmptyPage:
        all_products = paginator.page(paginator.num_pages)  # ✅ Correct usage

    context = {
        'search_query': search_query,
        'all_products': all_products,
    }
    request_type = request.GET.get('request_type')
    if request_type == 'htmx':
        return render(request, 'management/products/htmx/product_user_table.html', context)
    return render(request, 'management/products/product_list.html', context)


def add_product(request):
    category = Category.objects.all()
    vendor = Vendor.objects.all()
    tags = Tag.objects.all()

   
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        product_name = request.POST.get('product_name') 
        description = request.POST.get('description') 
        price = request.POST.get('price') 
        product_image = request.FILES.get('product_image')
        tag_ids = request.POST.getlist('tag_id')
        rating = request.POST.get('rating')
        vendor_id = request.POST.get('vendor_id')
   
        #print(category_id,product_name,description,price,product_image,tag_ids,rating,vendor_id)

       
        if category_id and product_name and description and price and tags and rating and vendor_id :
            tag_ids = [int(tag_id) for tag_id in tag_ids if tag_id.isdigit()]
            tags = Tag.objects.filter(id__in=tag_ids)
           
            product = Product.objects.create(
                category_id = category_id,
                product_name=product_name, 
                description=description, 
                price=price, 
                product_image=product_image,
                rating=rating,
                vendor_id=vendor_id,
            
            )
            product.tags.set(tags)
            product.save()
            messages.success(request,'Product added sucessful')
            return redirect('products')
        else:
            messages.error(request, 'All Fields Are Requerds')
        
        
    context = {
        'category': category,
        'vendor' :  vendor,
        'tags' : tags,
    }
    return render(request, 'management/add_product.html',context)


def edit_product(request,id):
    product = get_object_or_404(Product, id=id)
    category = Category.objects.all()
    vendor = Vendor.objects.all()
    tags = Tag.objects.all()
    
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        product_name = request.POST.get('product_name') 
        description = request.POST.get('description') 
        price = request.POST.get('price') 
        product_image = request.FILES.get('product_image')
        tag_ids = request.POST.getlist('tag_id')  # Fix multi-select
        rating = request.POST.get('rating')
        vendor_id = request.POST.get('vendor_id')
        date = request.POST.get('date')

        if category_id and product_name and description and price and rating and vendor_id:
            product.category_id = int(category_id)
            product.product_name = product_name
            product.description = description
            product.price = price
            if product_image:  # Only update if a new image is provided
                product.product_image = product_image
            product.rating = rating
            if date:  # Only update if date is provided
                product.date = date

            product.tags.set(Tag.objects.filter(id__in=tag_ids))  # Fix tags
            product.save()
            return redirect('products')
    context = {
        'category': category,
        'vendor' :  vendor,
        'tags' : tags,
        'product':product
    }
    
    return render(request,'management/edit_product.html',context)

def delete_product(request, id):
    product = get_object_or_404(Product, id=id) 
    product.delete()
    return redirect(products)

def product_view(request):
    product = get_object_or_404(Product, id=id)   
    return render(request, 'management/product_list.html', {'product': product})


    