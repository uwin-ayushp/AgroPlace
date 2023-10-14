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
# Create your views here.
"""verification email"""
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def products(request):
    # Your view logic here
    return render(request, 'products.html')
