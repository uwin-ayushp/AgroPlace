import random
from django.shortcuts import get_object_or_404

import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from store.models import Product, ReviewRating

from category.models import Category
from .forms import ReviewForms, ProductSortForm ,CatSortForm
from django.contrib import messages
 
def store(request, category_slug=None):
    products = None
    products_count = None
    s_product = None
    c_product = None
    if request.method == 'POST':
        form = ProductSortForm(request.POST)
        c_form = CatSortForm(request.POST)
        if c_form.is_valid():
            selected_cat = c_form.cleaned_data['csort']
            c_product = Product.objects.all().filter(is_available=True)
            c_product = apply_catsorting(c_product, selected_cat)

        if form.is_valid():
            selected_sort = form.cleaned_data['sort']
            # s_product = Product.objects.all().filter(is_available=True)
            # print(selected_sort)
            s_product = apply_sorting(c_product, selected_sort)




    categories = None

    query = request.GET.get('q',None)
    category_query = request.GET.get('category',None)
    if category_query:
        try:
            categories = Category.objects.get(category_name=category_query)
            products = Product.objects.filter(category=categories,is_available=True)
            products_count = products.count()
        except:
            pass
    elif query:
        products = Product.objects.filter(product_name__icontains=query)
        products_count = products.count()
    elif s_product:
        products = s_product
        products_count = products.count()
    elif c_product:
        products = c_product
        print(products)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        products_count  = products.count()

    # print(products)
    form = ProductSortForm(request.GET)
    catform = CatSortForm(request.GET)
    context = {
        'products': products,
        'products_count' :products_count,
        'form': form,
        'catform':catform,
    }
    return render(request, 'store/store.html',context)

 

def submit_reviews(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForms(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you, your Review has been updated')
            return redirect(url)


        except ReviewRating.DoesNotExist:
            form = ReviewForms(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you, your Review has been submitted')
                return redirect(url)


def get_random_products():
    all_products = list(Product.objects.all())
    random.shuffle(all_products)
    return all_products

def get_recommendations(request):
    product_names = ["Potatoes", "Wheat", "Broccoli", "Carrots", "Onions"]
    recommendations = list(Product.objects.filter(product_name__in=product_names))
    random.shuffle(recommendations)

    context = {
        'recommendations': recommendations
    }
    return render(request, 'store/recommended_products.html', context)

def sortProducts(request):
    return store(request)

def catProducts(request):
    return store(request)

def apply_sorting(queryset, sort_by):
    # Apply sorting logic based on the 'sort_by' parameter
    if sort_by == 'new':
        return queryset.order_by('-created_date')
    elif sort_by == 'price_low_to_high':
        print('enterd')
        return queryset.order_by('price')
    elif sort_by == 'price_high_to_low':
        return queryset.order_by('-price')
    elif sort_by == 'category':
        return queryset.order_by('-category')
    else:
        return queryset  # Default sorting



def apply_catsorting(queryset, sort_by):
    if sort_by == 'allproducts':
        return queryset
    elif sort_by == 'fruits':
        category = get_object_or_404(Category, category_name='Fruits')
        return queryset.filter(category=category.id)
    elif sort_by == 'grains':
        category = get_object_or_404(Category, category_name='Grains')
        return queryset.filter(category=category.id)
    elif sort_by == 'seeds':
        category = get_object_or_404(Category, category_name='Seeds')
        return queryset.filter(category=category.id)
    elif sort_by == 'vegetable':
        category = get_object_or_404(Category, category_name='Vegetables')
        return queryset.filter(category=category.id)
    else:
        return queryset.none()  # Return an empty queryset if 'sort_by' is not recognized
