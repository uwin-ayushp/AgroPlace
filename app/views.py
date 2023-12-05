from django.shortcuts import render
from store.models import Product, ReviewRating, ProductGalary
from django.views.generic import DetailView
from orders.models import OrderProduct,Account
from django.http import JsonResponse
from django.core.cache import cache
import random

def get_random_products():
    all_products = list(Product.objects.all())
    return random.sample(all_products, min(4, len(all_products)))

def home(request):
    products = Product.objects.all().filter(is_available=True)
    recommended_products = get_random_products()
    context = {
        'products': products,
        'recommended_products': recommended_products
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, product_id=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['reviews'] = ReviewRating.objects.filter(product_id=self.object.id, status=True)
        context['product_galary'] = ProductGalary.objects.filter(product_id=self.object.id)
        context['all_products'] = Product.objects.all()[0:4]

        if self.request.user.is_authenticated:
            try:
                context['orderproduct'] = OrderProduct.objects.filter(user=self.request.user,
                                                                      product_id=self.object.id).exists()
            except OrderProduct.DoesNotExist:
                orderproduct = None
        else:
            orderproduct = None

        return context




