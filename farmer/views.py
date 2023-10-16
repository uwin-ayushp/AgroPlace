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
from store.models import Product
from app.models import Account
def products(request):
    farmerid = Account.objects.get(email=request.user)
    products = Product.objects.filter(farmerID=farmerid.id)
    return render(request, 'products.html', {'products': products})

@login_required(login_url='login')
def add_products(request):
    add_product_form = AddProductForm()
    # if request.method == "POST":
    #     form = AddProductForm(request.POST)
    #     if form.is_valid():
    #         product_name = form.cleaned_data['product_name']
    #
    #     context = {
    #         'form': form
    #     }
    return render(request, 'add_product.html', {'add_product_form' : add_product_form})


   




# class ProductListView(ListView):
#     model = Product
#     template_name = 'products/products.html'
#     context_object_name = 'products'

