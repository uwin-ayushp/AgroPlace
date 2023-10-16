from django.urls import path
from .import views
from .views import ProductListView

app_name='farmer'

urlpatterns = [
    path('products/', views.products,name='products' ),
    path('add_products/', views.add_products, name='add_products')
]