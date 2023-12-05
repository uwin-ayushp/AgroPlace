import joblib as joblib
import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from django.urls import reverse
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

from orders.models import Order
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

def expert_advice(request):
    sp = Account.objects.filter(user_role='specialist')
    return render(request, 'expert_advice.html', {'sp': sp})

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

@login_required(login_url='login')
def farmerOrder(request, user_id):
    orders = Order.objects.filter(farmer_id=user_id).order_by('-status', 'created_at')

    status = orders.first().status
    context = {
        'orders': orders,
        'order_status':status
    }
    return render(request, 'order.html',context)

@login_required(login_url='login')
def change_status(request, order_id):
    if request.method == 'POST':
        userid = request.user.id
        new_status = request.POST.get('status')  # Use the correct field name
        order =Order.objects.get(id=order_id)
        order.status = new_status
        order.save()

        # You can redirect to the order list or any other page
        return redirect('farmer:farmerOrder', user_id=userid)


    return HttpResponse("Bad Request", status=400)

# Load the pre-trained model and data
model = joblib.load('farmer/model/product_trending_model.pkl')
model2 = joblib.load('farmer/model/recommendation_model.pkl')
df = pd.read_csv('farmer/model/AgroPlace_Dataset_6.csv')
reader = Reader(rating_scale=(0, 10))
data = Dataset.load_from_df(df[['Customer ID', 'Product line', 'Rating']], reader)
trainset = data.build_full_trainset()
input = [
    [74.69, 7, 26.1415, 548.9715, 522.83, 4.761904762, 26.1415, 9.1],
    [55.59, 5, 12.2475, 257.2475, 245, 4.761904762, 12.2475, 8.8],
]

def insights(request):
    trending_products_list = [('Potatoes', 63), ('Wheat', 45), ('Broccoli', 39), ('Carrots', 35), ('Onions', 33)]

    context = {
        'trending_products_list': trending_products_list,
    }

    return render(request, 'insights.html', context)