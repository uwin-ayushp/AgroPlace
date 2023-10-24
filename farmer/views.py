from django.shortcuts import render, redirect,get_object_or_404
# from .forms import RegistrationForm, UserForm, UserProfileForm
from app.models import Account, UserProfile
# from orders.models import Order, OrderProduct
# from cart.models import Cart, CartItem
# from cart.views import _cart_id
import requests
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import AddProductForm
# Create your views here.
"""verification email"""
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.views.generic import ListView
from category.models import Category
from store.models import Product
from app.models import Account
from django import forms
def products(request):
    farmerid = Account.objects.get(email=request.user)
    products = Product.objects.filter(farmerID=farmerid.id)
    return render(request, 'products.html', {'products': products})


@login_required(login_url='login')
def add_products(request):
    if request.method == "POST":
        add_product_form = AddProductForm(request.POST,
                                          request.FILES)  # Pass request.FILES to handle image file uploads

        if add_product_form.is_valid():
            # Retrieve form data
            product_name = add_product_form.cleaned_data['product_name']
            description = add_product_form.cleaned_data['description']
            price = add_product_form.cleaned_data['price']
            image = add_product_form.cleaned_data['image']
            category = add_product_form.cleaned_data['category']
            quantity = add_product_form.cleaned_data['quantity']


            # Create and save a new Product instance
            new_product = Product(
                farmerID=request.user.id,  # Assuming you want to associate the product with the logged-in user
                product_name=product_name,
                description=description,
                price=price,
                image=image,
                category=category,
                quantity=quantity
                # Add other fields as needed
            )
            new_product.save()

            # You can perform additional actions or redirection here

    else:
        add_product_form = AddProductForm()

    return render(request, 'add_product.html', {'add_product_form': add_product_form})

@login_required(login_url='login')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Save the updated product data
            return redirect('farmer:products')
    else:
        form = AddProductForm(instance=product)

    context = {
        'form' : form,
        'product_id' : product_id
    }

    return render(request, 'edit_product.html', context)


@login_required(login_url='login')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('farmer:products')