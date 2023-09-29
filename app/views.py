from django.shortcuts import render
from django.views.generic import  DetailView
from django.http import JsonResponse
from django.core.cache import cache


def home(request):
    # products = Product.objects.all().filter(is_available=True)
    # context = {
    #     'products' : products,
    # }
    return render(request, 'home.html')

   
    
